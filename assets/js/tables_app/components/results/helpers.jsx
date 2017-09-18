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
  />)
}

function columnHelper(column_list) {
  let columns = [{
    Header: '',
    accessor: 'race/ethnicity'
  }];
  column_list.forEach((column_name) => {
    let column = {
      Header: column_name,
      columns: [{
        Header: 'Stops',
        id: column_name + 'count',
        accessor: d => d[column_name]['count'],
        maxWidth: 200
      }, {
        Header: 'Percent',
        id: column_name + 'percent',
        accessor: d => d[column_name]['percent'],
        maxWidth: 200
      }]
    }
    columns.push(column)
  });

  return columns;
}


export function buildStopTable(data) {
  const columns = [{
    Header: '',
    accessor: 'race/ethnicity',
    maxWidth: 400
  }, {
    Header: 'Count',
    accessor: 'count',
    maxWidth: 200
  }, {
    Header: 'Percent',
    accessor: 'percent',
    maxWidth: 200
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

export function buildAgeOfDriverTable(data) {
  const columns = [{
    Header: '',
    accessor: 'race/ethnicity'
  }, {
    Header: '16 to 25',
    columns: [{
      'Header': 'Stops',
      'id': 'count16',
      'accessor': d => d['16 to 25']['count']
    },{
      'Header': 'Percent',
      'id': 'percent16',
      'accessor': d => d['16 to 25']['percent']
    }]
  }, {
    Header: '25 to 40',
    columns: [{
      'Header': 'Stops',
      'id': 'count25',
      'accessor': d => d['25 to 40']['count']
    },{
      'Header': 'Stops',
      'id': 'percent25',
      'accessor': d => d['25 to 40']['percent']
    }]
  }, {
    Header: '40 to 60',
    columns: [{
      'Header': 'Stops',
      'id': 'count40',
      'accessor': d => d['40 to 60']['count']
    },{
      'Header': 'Stops',
      'id': 'percent40',
      'accessor': d => d['40 to 60']['percent']
    }]
  }, {
    Header: '60+',
    columns: [{
      'Header': 'Stops',
      'id': 'count60',
      'accessor': d => d['60+']['count']
    },{
      'Header': 'Stops',
      'id': 'percent60',
      'accessor': d => d['60+']['percent']
    }]
  }];

  return makeTable(columns, data)
}

export function buildDispositionTable(data) {
  const columns = [{
    Header: '',
    accessor: 'race/ethnicity'
  }, {
    Header: 'UAR',
    columns: [{
      'Header': 'Stops',
      'id': 'countUAR',
      'accessor': d => d['UAR']['count']
    },{
      'Header': 'Percent',
      'id': 'percentUAR',
      'accessor': d => d['UAR']['percent']
    }]
  }, {
    Header: 'Mis. Summons',
    columns: [{
      'Header': 'Stops',
      'id': 'countSum',
      'accessor': d => d['Mis. Summons']['count']
    },{
      'Header': 'Percent',
      'id': 'percentSum',
      'accessor': d => d['Mis. Summons']['percent']
    }]
  }, {
    Header: 'Infraction',
    columns: [{
      'Header': 'Stops',
      'id': 'countInf',
      'accessor': d => d['Infraction']['count']
    },{
      'Header': 'Percent',
      'id': 'percentInf',
      'accessor': d => d['Infraction']['percent']
    }]
  }, {
    Header: 'Written Warning',
    columns: [{
      'Header': 'Stops',
      'id': 'countWarn',
      'accessor': d => d['Written Warning']['count']
    },{
      'Header': 'Percent',
      'id': 'percentWarn',
      'accessor': d => d['Written Warning']['percent']
    }]
  },  {
    Header: 'Verbal Warning',
    columns: [{
      'Header': 'Stops',
      'id': 'countVWarn',
      'accessor': d => d['Verbal Warning']['count']
    },{
      'Header': 'Percent',
      'id': 'percentVWarn',
      'accessor': d => d['Verbal Warning']['percent']
    }]
  }];

  return makeTable(columns, data)
}


export function buildSearchInformationTable(data) {
   const column_names = ['Cars Searched', 'Consent', 'Inventory', 'Other', 'Contraband Found'];
   const columns = columnHelper(column_names);

  return makeTable(columns, data)
}
