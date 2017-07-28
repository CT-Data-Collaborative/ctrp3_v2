import React from 'react';
import { buildNatureOfStopTable, buildStopTable, buildStopsByMonthTable, buildStopsByHourTable, buildStopEnforcementMethodTable } from './helpers.jsx';

class Results extends React.Component {
  constructor(props) {
    super(props);
    const display = {};
    Object.keys(props.apiData).forEach((key) => display[key] = false);
    this.state = {
      display: display
    }
  }


  trafficStopTable(data) {
    if (this.state.display['Traffic Stops'] == true) {
      return buildStopTable(data['Traffic Stops'])
    } else {
      return <div></div>
    }
  }

  stopEnforcementTable(data) {
    if (this.state.display['Stop Enforcement Method'] == true) {
      return buildStopEnforcementMethodTable(data['Stop Enforcement Method'])
    } else {
      return <div></div>
    }
  }

  natureOfStopsTable(data) {
    if (this.state.display['Nature of the Traffic Stop'] == true) {
      return buildNatureOfStopTable(data['Nature of the Traffic Stop'])
    } else {
      return <div></div>
    }
  }

  stopsByMonthTable(data) {
    if (this.state.display['Stops by Month'] == true) {
      return buildStopsByMonthTable(data['Stops by Month'])
    } else {
      return <div></div>
    }
  }

  stopsByHourTable(data) {
    if (this.state.display['Stops by Hour'] == true) {
      return buildStopsByHourTable(data['Stops by Hour'])
    } else {
      return <div></div>
    }
  }

  componentWillReceiveProps(nextProps) {
    let display = {};

    Object.keys(nextProps.apiData).forEach((key) => {
      if (nextProps.apiData[key].length > 0) {
        display[key] = true;
      } else {
        display[key] = false;
      }
    });


    this.setState({ display })
  }

  displayList() {
    const display = this.state.display;
    return <ul>{Object.keys(display).map((l) => <li key={l}>{l}: {display[l] ? 'True' : 'False'}</li>)}</ul>
  }

  render() {
    return (
      <div>
        <h3>Results</h3>
        {this.trafficStopTable(this.props.apiData)}
        {this.stopEnforcementTable(this.props.apiData)}
        {this.natureOfStopsTable(this.props.apiData)}
        {this.stopsByMonthTable(this.props.apiData)}
        {this.stopsByHourTable(this.props.apiData)}
      </div>)

  }
}

export default Results;
