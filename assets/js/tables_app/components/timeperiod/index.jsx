import React from 'react';
import Select from 'react-select';

class DateRange extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      months: props.months,
      startMonth: props.months[0],
      endMonth: props.months[props.months.length-1]
    };
    this.setStartMonth = this.setStartMonth.bind(this);
    this.setEndMonth = this.setEndMonth.bind(this);
  }

  setStartMonth(val) {
    this.props.selectStartDate(val.value);
    this.setState({ startMonth: val.value });
  }

  setEndMonth(val) {
    this.props.selectEndDate(val.value);
    this.setState({ endMonth: val.value });
  }

  render() {
    const startMonths = this.state.months.map((d) => {
      return { value: d, label: d };
    });

    // limit the end month choices to those months greater than the currently
    // selected start month
    const i = startMonths.findIndex(x => x.value == this.state.startMonth);
    const endMonths = startMonths.slice(i+1,startMonths.length);

    return (
      <div>
        <h5>Start Month</h5>
        <Select
          name="start-month-select"
          value={this.state.startMonth}
          options={startMonths}
          onChange={this.setStartMonth}
        />
      <h5>End Month</h5>
        <Select
          name="end-month-select"
          value={this.state.endMonth}
          options={endMonths}
          onChange={this.setEndMonth}
        />
      </div>
    );
  }
}

export default DateRange;
