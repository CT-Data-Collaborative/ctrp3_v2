import React from 'react';
import ReactTable from 'react-table'


function makeTable(columns, data) {
  return (<ReactTable
    className="-striped -highlight"
    data={data}
    columns={columns}
    showPaginationBottom={false}
    showPageSizeOptions={false}
    showPagination={false}
    defaultPageSize={data.length}
    style={{
        height: '400px' // This will force the table body to overflow and scroll, since there is not enough room
    }}
  />)
}

export function buildStopTable(data) {
  const columns = [{
    Header: '',
    accessor: 'race/ethnicity'
  }, {
    Header: 'Count',
    accessor: 'count'
  }, {
    Header: 'Percent',
    accessor: 'percent'
  }];

  return makeTable(columns, data)
}

export function buildStopEnforcementMethodTable(data) {
  const columns = [{
    Header: 'Enforcement Method',
    accessor: 'column'
  }, {
    Header: 'Count',
    accessor: 'count'
  }, {
    Header: 'Percent',
    accessor: 'percent'
  }];

  return makeTable(columns, data)
}

export function buildStopsByHourTable(data) {
  const columns = [{
    Header: 'Hour',
    accessor: 'hour'
  }, {
    Header: 'Stops',
    accessor: 'count'
  }];

  return makeTable(columns, data)
}

export function buildStopsByMonthTable(data) {
  const columns = [{
    Header: 'Month',
    accessor: 'month'
  }, {
    Header: 'Stops',
    accessor: 'count'
  }];

  return makeTable(columns, data)
}

export function buildResidencyTable(data) {
  const columns = [{
    Header: '',
    accessor: 'column'
  },{
    Header: 'Stops',
    accessor: 'count'
  }, {
    Header: 'Percent',
    accessor: 'percent'
  }];

  return makeTable(columns, data)
}

export function buildNatureOfStopTable(data) {
  const columns = [{
    Header: '',
    accessor: 'race/ethnicity'
  }, {
    Header: 'Investigative',
    columns: [{
      'Header': 'Stops',
      'id': 'investigativeCount',
      'accessor': d => d['Investigative']['count']
    }, {
      'Header': 'Percent',
      'id': 'investigativePercent',
      'accessor': d => d['Investigative']['percent']
    }]
  }, {
    Header: 'Equipment',
    columns: [{
      'Header': 'Stops',
      'id': 'equipmentCount',
      'accessor': d => d['Equipment']['count']
    }, {
      'Header': 'Percent',
      'id': 'equipmentCount',
      'accessor': d => d['Equipment']['percent']
    }]
  }, {
    Header: 'Motor Vehicle',
    columns: [{
      'Header': 'Stops',
      'id': 'mvCount',
      'accessor': d => d['Motor Vehicle']['count']
    }, {
      'Header': 'Percent',
      'id': 'mvPercent',
      'accessor': d => d['Motor Vehicle']['percent']
    }]
  }];

  return makeTable(columns, data)
}
