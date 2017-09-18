import React from 'react';
import {
  buildNatureOfStopTable,
  buildStopTable,
  buildStopsByMonthTable,
  buildStopsByHourTable,
  buildStopEnforcementMethodTable,
  buildAgeOfDriverTable,
  buildDispositionTable,
  buildResidencyTable,
  buildSearchInformationTable
} from './helpers.jsx';

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
      return (
        <div className="ctdata-ctrp3-results-table ctdata-ctrp3-results-table-md">
          <h4>Traffic Stops</h4>
          {buildStopTable(data['Traffic Stops'])}
        </div>
      )

    } else {
      return <div></div>
    }
  }

  stopEnforcementTable(data) {
    if (this.state.display['Stop Enforcement Method'] == true) {
      return (
        <div className="ctdata-ctrp3-results-table ctdata-ctrp3-results-table-md">
          <h4>Stop Enforcement Method</h4>
          {buildStopEnforcementMethodTable(data['Stop Enforcement Method'])}
        </div>
      )
    } else {
      return <div></div>
    }
  }

  natureOfStopsTable(data) {
    if (this.state.display['Nature of the Traffic Stop'] == true) {
      return (
        <div className="ctdata-ctrp3-results-table ctdata-ctrp3-results-table-lg">
          <h4>Nature of the Traffic Stop</h4>
          {buildNatureOfStopTable(data['Nature of the Traffic Stop'])}
        </div>
      )
    } else {
      return <div></div>
    }
  }

  stopsByMonthTable(data) {
    if (this.state.display['Stops by Month'] == true) {
      return (
        <div className="ctdata-ctrp3-results-table ctdata-ctrp3-results-table-sm">
          <h4>Stops by Month</h4>
          {buildStopsByMonthTable(data['Stops by Month'])}
        </div>
      )
    } else {
      return <div></div>
    }
  }

  stopsByHourTable(data) {
    if (this.state.display['Stops by Hour'] == true) {
      return (
        <div className="ctdata-ctrp3-results-table ctdata-ctrp3-results-table-sm">
          <h4>Stop by Hour</h4>
          {buildStopsByHourTable(data['Stops by Hour'])}
        </div>
      )
    } else {
      return <div></div>
    }
  }

  ageOfDriverTable(data) {
    if (this.state.display['Age of the Driver'] == true) {
      return (
        <div className="ctdata-ctrp3-results-table ctdata-ctrp3-results-table-lg">
          <h4>Age of the Driver</h4>
          {buildAgeOfDriverTable(data['Age of the Driver'])}
        </div>
      )
    } else {
      return <div></div>
    }
  }

  dispositionTable(data) {
    if (this.state.display['Disposition of the Traffic Stop'] == true) {
      return (
        <div className="ctdata-ctrp3-results-table ctdata-ctrp3-results-table-lg">
          <h4>Disposition of the Traffic Stop</h4>
          {buildDispositionTable(data['Disposition of the Traffic Stop'])}
        </div>
      )
    } else {
      return <div></div>
    }
  }

  residencyTable(data) {
    if (this.state.display['Residency Information'] == true) {
      return (
        <div className="ctdata-ctrp3-results-table ctdata-ctrp3-results-table-sm">
          <h4>Residency Information</h4>
          {buildResidencyTable(data['Residency Information'])}
        </div>)
    } else {
      return <div></div>
    }
  }

  searchInformationTable(data) {
    if (this.state.display['Search Information'] == true) {
      return (<div className="ctdata-ctrp3-results-table ctdata-ctrp3-results-table-lg">
        <h4>Search Information</h4>{buildSearchInformationTable(data['Search Information'])}</div>)
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


    this.setState({display})
  }

  render() {
    return (
      <div>
        {this.trafficStopTable(this.props.apiData)}
        {this.stopEnforcementTable(this.props.apiData)}
        {this.natureOfStopsTable(this.props.apiData)}
        {this.stopsByMonthTable(this.props.apiData)}
        {this.stopsByHourTable(this.props.apiData)}
        {this.ageOfDriverTable(this.props.apiData)}
        {this.dispositionTable(this.props.apiData)}
        {this.residencyTable(this.props.apiData)}
        {this.searchInformationTable(this.props.apiData)}
      </div>)

  }
}

export default Results;
