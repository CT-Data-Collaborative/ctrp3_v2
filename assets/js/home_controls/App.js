/**
 * Created by scuerda on 7/20/17.
 */
import React, {Component} from 'react';

import Department from '../components/department';
import DateRange from '../components/timeperiod';


class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      csrf: window.CSRF_TOKEN,
      startDate: window.months[0],
      endDate: window.months[window.months.length - 1],
    };
    this.updateSelectedDept = this.updateSelectedDept.bind(this);
    this.updateStartDate = this.updateStartDate.bind(this);
    this.updateEndDate = this.updateEndDate.bind(this);
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


  render() {
    return (
      <div className="row">
        <div className="col-md-6 offset-md-3">
          <div className="row ctdata-ctrp3-homepage-controls">
            <h3 className="ctdata-ctrp3-homepage-controls--header" >Explore by department and time period</h3>
            <Department departments={window.departments} selectDept={this.updateSelectedDept} width={'full'}/>
            <DateRange months={window.months} selectStartDate={this.updateStartDate}
                       selectEndDate={this.updateEndDate} width={'full'}/>

            <form action="/reports/tables/" method="post">
              <input type="hidden" name="csrfmiddlewaretoken" value={this.state.csrf}/>
              <input type="hidden" name="department" value={this.state.selectedDepartment}/>
              <input type="hidden" name="start_date" value={this.state.startDate}/>
              <input type="hidden" name="end_date" value={this.state.endDate}/>
              <input type="submit" value="Submit" />
            </form>
          </div>
          <div className="row">
            <h3 className="ctdata-ctrp3-homepage-controls--header">Download raw data by location</h3>
          </div>
        </div>
      </div>
    )
  }
}

export default App;
