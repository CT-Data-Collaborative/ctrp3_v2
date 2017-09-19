import React from 'react';
import Select from 'react-select';

class DateRange extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      months: props.months,
      startMonth: props.months[0],
      endMonth: props.months[props.months.length - 1]
    };
    this.setStartMonth = this.setStartMonth.bind(this);
    this.setEndMonth = this.setEndMonth.bind(this);
    this.layout = this.layout.bind(this);
  }

  setStartMonth(val) {
    this.props.selectStartDate(val.value);
    this.setState({startMonth: val.value});
  }

  setEndMonth(val) {
    this.props.selectEndDate(val.value);
    this.setState({endMonth: val.value});
  }

  layout(width) {
    const startMonths = this.state.months.map((d) => {
      return {value: d, label: d};
    });

    // limit the end month choices to those months greater than the currently
    // selected start month
    const i = startMonths.findIndex(x => x.value == this.state.startMonth);
    const endMonths = startMonths.slice(i + 1, startMonths.length);

    if (width == 'full') {
      return (
        <div className="col-sm-12 ctdata-ctrp3-selector">
          <h4>Time Period</h4>
          <hr/>
          <div className="row">
            <div className="col-md-5">
              <Select
                name="start-month-select"
                value={this.state.startMonth}
                options={startMonths}
                onChange={this.setStartMonth}
              />
            </div>
            <div className="col-md-1">
              <p className="ctdata-ctrp3-date-selector-joiner">to</p>
            </div>
            <div className="col-md-6">
              <Select
                name="end-month-select"
                value={this.state.endMonth}
                options={endMonths}
                onChange={this.setEndMonth}
              />
            </div>
          </div>
        </div>
      )
    } else {
      return (
        <div className="row">
          <div className="col-md-12 ctdata-ctrp3-selector">
            <h4>Time Period</h4>
            <hr/>
          </div>
          <div className="col-md-5">
            <Select
              name="start-month-select"
              value={this.state.startMonth}
              options={startMonths}
              onChange={this.setStartMonth}
            />
          </div>
          <div className="col-md-1">
            <p className="ctdata-ctrp3-date-selector-joiner">to</p>
          </div>
          <div className="col-md-6">
            <Select
              name="end-month-select"
              value={this.state.endMonth}
              options={endMonths}
              onChange={this.setEndMonth}
            />
          </div>
        </div>
      );
    }
  }

  render() {
    return (this.layout(this.props.width));
  }
}

export default DateRange;
