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
  buildSearchInformationTable,
  buildStopAuthorityTable
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
          <h5>Traffic Stops</h5>
          <p>Summary of traffic stops by race, ethnicity and gender.</p>
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
        <div className="ctdata-ctrp3-results-table ctdata-ctrp3-results-table-sm">
          <h5>Stop Enforcement Method</h5>
          <p>Summarizes the enforcement method used to conduct the traffic stop. Blind Enforcement include for example: radar/laser, license plate readers, DUI checkpoints, and truck weighing operations. Spot check includes: seat belt use, cellphone use, or any other activity except DUI checks. For Spot checks, traffic stop information is only collected when action is taken. General includes all other stops. Percentages are derived from the total number of people stopped.</p>
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
          <h5>Nature of the Traffic Stop</h5>
          <p>Police are required to identify the nature of the stop in one of three categories: 1) Investigative, Criminal; 2) Violation, Motor Vehicle; or 3) Equipment, Motor Vehicle.</p>
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
          <h5>Age of the Driver</h5>
          <p>Summarizes the age of the driver stopped into four age groups by race and ethnicity. Percentages are derived from the total number of people stopped.</p>
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
          <h5>Residency Information</h5>
          <p>Stopped driver residency information. Percentages are derived from the total number of people.</p>
          {buildResidencyTable(data['Residency Information'])}
        </div>)
    } else {
      return <div></div>
    }
  }

  searchInformationTable(data) {
    if (this.state.display['Search Information'] == true) {
      return (
        <div className="ctdata-ctrp3-results-table ctdata-ctrp3-results-table-lg">
          <h5>Search Information</h5>
          <p>Summarizes car searches, the authority for the search and whether contraband was found as a result of the search. Percentages are derived from the total number of people stopped for each race/ethnicity.</p>
          {buildSearchInformationTable(data['Search Information'])}</div>)
    } else {
      return <div></div>
    }
  }


  statutoryAuthorityTable(data) {
    if (this.state.display['Statutory Authority Cited for Stop'] == true) {
      return (
        <div className="ctdata-ctrp3-results-table ctdata-ctrp3-results-table-lg">
          <h5>Statutory Authority Cited for Stop</h5>
          <p>Police officers are required to identify the statutory authority for the stop. These categories are
            aggregations. In addition, these categories do not reflect additional citations issued during the course of the stop.</p>
          {buildStopAuthorityTable(data['Statutory Authority Cited for Stop'])}
        </div>

      )
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
        {this.statutoryAuthorityTable(this.props.apiData)}
      </div>)

  }
}

export default Results;
