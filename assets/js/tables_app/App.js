/**
 * Created by scuerda on 7/20/17.
 */
import React, { Component } from 'react';

import Department from './components/department';
import DateRange from './components/timeperiod';
import Links from './components/links';
import Results from './components/results';

class App extends Component {
  constructor(props) {
    super(props);

    this.state = {
      selectedDepartment: null,
      startDate: window.months[0],
      endDate: window.months[window.months.length - 1],
      apiLinks: window.api_links,
      apiData: window.apiData,
      selectedAnalyses: []
    };


    this.updateSelectedDept = this.updateSelectedDept.bind(this);
    this.updateStartDate = this.updateStartDate.bind(this);
    this.updateEndDate = this.updateEndDate.bind(this);
    this.updateData = this.updateData.bind(this);
    this.getData = this.getData.bind(this);
    this.updateSelectedAnalyses = this.updateSelectedAnalyses.bind(this)
  }

  componentDidUpdate(prevProps, prevState) {
    // This approach will have a slight issue in that changing department type will trigger a full load
    if (this.state.selectedDepartment != prevState.selectedDepartment) {
      this.getData(this.state.selectedDepartment, this.state.startDate, this.state.endDate, this.state.selectedAnalyses)
    }
    if (this.state.startDate != prevState.startDate) {
      this.getData(this.state.selectedDepartment, this.state.startDate, this.state.endDate, this.state.selectedAnalyses)
    }
    if (this.state.endDate != prevState.endDate) {
      this.getData(this.state.selectedDepartment, this.state.startDate, this.state.endDate, this.state.selectedAnalyses)
    }
    if (this.state.selectedAnalyses != prevState.selectedAnalyses) {
      this.getData(this.state.selectedDepartment, this.state.startDate, this.state.endDate, this.state.selectedAnalyses)
    }
  }

  buildQString(params) {
    const esc = encodeURIComponent;
    return Object.keys(params)
      .map(k => esc(k) + '=' + esc(params[k]))
      .join('&');
  }

  fetchData(url, item) {
    return new Promise((resolve, reject) => {
      const cachedData = sessionStorage.getItem(url);

      if (cachedData) {
        resolve({ 'name': item, 'data': JSON.parse(cachedData) });
      }
      else {
        fetch(url)
          .then((response) => {
          if (response.status >= 400) {
            reject(response.status, "Bad response from server");
          }
          return response.json();
          })
          .then((data) => {
            sessionStorage.setItem(url, JSON.stringify(data));
            resolve({ 'name': item, 'data': data })
          })
      }

    });
  }

  // TODO set up server side cache to handle already requested urls
  getData(dept, start, end, analyses) {

    // Kinda wonky, but otherwise this.updateData is not available from within Promise.all().then()
    const updateData = this.updateData;

    let params = {
      dateStart: start,
      dateEnd: end
    };

    if (dept !== null) {
      params['department'] = dept;
    }

    let qStr = this.buildQString(params);

    // reset the api data to empty array
    const apiData = {};

    Object.keys(this.state.apiData).forEach((key) => {
      apiData[key] = [];
    });


    const urlPromises = analyses.map((item) => {
      const url = this.state.apiLinks[item] + '?' + qStr;
      return this.fetchData(url, item);
    });


    Promise.all(urlPromises)
      .then(function(results) {
        results.forEach((r) => {
          apiData[r.name] = r.data;
        });
        updateData(apiData)
      })
      .catch(function(err) {
        console.log("Failed: ", err);
      });


  }

  updateSelectedDept(d) {
    this.setState({ selectedDepartment: d });
  }

  updateStartDate(d) {
    this.setState({ startDate: d });
  }

  updateEndDate(d) {
    this.setState({ endDate: d });
  }

  updateSelectedAnalyses(selectedAnalyses) {
    this.setState({ selectedAnalyses });
  }

  updateData(newData) {
    this.setState({ apiData: newData });
  }

  infoHeader() {
    const selectedDept = this.state.selectedDepartment;
    const startDate = this.state.startDate;
    const endDate = this.state.endDate;
    if (selectedDept) {
      return <h3>{selectedDept}, {startDate} to {endDate}</h3>
    } else {
      return <h3>All Stops, {startDate} to {endDate}</h3>
    }
  }

  render() {
    return (
      <div className="ctdata-ctrp3-app">
        <div className="row">
          <div className="col col-md-2">
            <Department
              departments={window.departments}
              selectDept={this.updateSelectedDept}
            />
            <DateRange
              months={window.months}
              selectStartDate={this.updateStartDate}
              selectEndDate={this.updateEndDate}
            />
            <Links
              apiLinks={this.state.apiLinks}
              updateAnalyses={this.updateSelectedAnalyses}
            />
          </div>
          <div className="col-md-auto">
            <h2>Explore Stop Data by Departments</h2>
            {this.infoHeader()}
            <Results
              apiData={this.state.apiData}
            />
          </div>
        </div>
      </div>
    );
  }
}

export default App;
