/**
 * Created by scuerda on 7/20/17.
 */
import React, {Component} from 'react';

import Department from '../components/department';
import DateRange from '../components/timeperiod';
import Results from '../components/results';

class App extends Component {
  constructor(props) {
    super(props);

    this.state = {
      selectedDepartment: window.selected_department ? window.selected_department : null,
      startDate: window.start_date ? window.start_date : window.months[0],
      endDate: window.end_date ? window.end_date : window.months[window.months.length - 1],
      apiLinks: window.api_links,
      apiData: window.apiData,
      selectedAnalyses: Object.keys(window.apiData)
    };


    this.updateSelectedDept = this.updateSelectedDept.bind(this);
    this.updateStartDate = this.updateStartDate.bind(this);
    this.updateEndDate = this.updateEndDate.bind(this);
    this.updateData = this.updateData.bind(this);
    this.getData = this.getData.bind(this);
  }

  componentDidMount() {
    if (this.state.selectedDepartment != null) {
      this.getData(this.state.selectedDepartment, this.state.startDate, this.state.endDate, this.state.selectedAnalyses)
    }
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
        resolve({'name': item, 'data': JSON.parse(cachedData)});
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
            resolve({'name': item, 'data': data})
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
      .then(function (results) {
        results.forEach((r) => {
          apiData[r.name] = r.data;
        });
        updateData(apiData)
      })
      .catch(function (err) {
        console.log("Failed: ", err);
      });


  }

  updateSelectedDept(d) {
    this.setState({selectedDepartment: d});
  }

  updateStartDate(d) {
    this.setState({startDate: d});
  }

  updateEndDate(d) {
    this.setState({endDate: d});
  }

  updateData(newData) {
    this.setState({apiData: newData});
  }

  infoHeader() {
    const selectedDept = this.state.selectedDepartment;
    const startDate = this.state.startDate;
    const endDate = this.state.endDate;
    if (selectedDept) {
      return (<div className="ctdata-ctrp3-results-info"><h4>{selectedDept} Police Department</h4><h5>{startDate} to {endDate}</h5></div>)
    } else {
      return <p/>
    }
  }

  render() {
    return (
      <div className="ctdata-ctrp3-app">
        <div className="row">
          <div className="col-sm-12 col-xl-3 ctdata-ctrp3-controls">
            <Department
              selectedDepartment={this.state.selectedDepartment}
              departments={window.departments}
              selectDept={this.updateSelectedDept}
            />
            <DateRange
              months={window.months}
              selectedStartDate={this.state.startDate}
              selectedEndDate={this.state.endDate}
              selectStartDate={this.updateStartDate}
              selectEndDate={this.updateEndDate}
            />
          </div>
          <div className="col-sm-12 col-xl-9 ctdata-ctrp3-results">
              {this.infoHeader()}
              <Results apiData={this.state.apiData} />
          </div>
        </div>
      </div>
    );
  }
}

export default App;
