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

function percentCellHelper(value) {
  if (+value == -999) {
    return '-';
  } else {
    return value + '%';
  }
}

function countCellHelper(value) {
  if (+value == -999) {
    return '-';
  } else {
    const intValue = +value
    return intValue.toLocaleString();
  }
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
        Cell: row => (
          <div>{countCellHelper(row.value)}</div>
        )
      }, {
        Header: 'Percent',
        id: column_name + 'percent',
        accessor: d => d[column_name]['percent'],
        Cell: row => (
          <div>{percentCellHelper(row.value)}</div>
        )
      }]
    }
    columns.push(column)
  });

  return columns;
}

function simpleColumnHelper(column_list, first_column_accessor) {
  let columns = [{
    Header: '',
    accessor: first_column_accessor
  }];
  column_list.forEach((column_name) => {
    let column = {
      Header: column_name,
      id: column_name + 'percent',
      accessor: d => d[column_name]['percent'],
      Cell: row => (
        <div>{percentCellHelper(row.value)}</div>
      )

    };
    columns.push(column);
  });
  return columns;
}


export function buildStopTable(data) {
  const columns = [{
    Header: '',
    accessor: 'race/ethnicity',
    minWidth: 300
  }, {
    Header: 'Count',
    accessor: 'count',
    Cell: row => (
      <div>{countCellHelper(row.value)}</div>
    )
  }, {
    Header: 'Percent',
    accessor: 'percent',
    Cell: row => (
        <div>{percentCellHelper(row.value)}</div>
      )
  }];

  return makeTable(columns, data)
}


export function buildStopEnforcementMethodTable(data) {
  const columns = [{
    Header: 'Enforcement Method',
    accessor: 'column',
    minWidth: 200
  }, {
    Header: 'Count',
    accessor: 'count',
    Cell: row => (
          <div>{countCellHelper(row.value)}</div>
        )
  }, {
    Header: 'Percent',
    accessor: 'percent',
    Cell: row => (
        <div>{percentCellHelper(row.value)}</div>
      )
  }];

  return makeTable(columns, data)
}

export function buildStopsByHourTable(data) {
  const columns = [{
    Header: 'Hour',
    accessor: 'hour'
  }, {
    Header: 'Stops',
    accessor: 'count',
    Cell: row => (
          <div>{countCellHelper(row.value)}</div>
        )
  }];

  return makeTable(columns, data)
}

export function buildStopsByMonthTable(data) {
  const columns = [{
    Header: 'Month',
    accessor: 'month'
  }, {
    Header: 'Stops',
    accessor: 'count',
    Cell: row => (
          <div>{countCellHelper(row.value)}</div>
        )
  }];

  return makeTable(columns, data)
}

export function buildResidencyTable(data) {
  const columns = [{
    Header: '',
    accessor: 'column'
  },{
    Header: 'Stops',
    accessor: 'count',
    Cell: row => (
          <div>{countCellHelper(row.value)}</div>
        )
  }, {
    Header: 'Percent',
    accessor: 'percent',
    Cell: row => (
        <div>{percentCellHelper(row.value)}</div>
      )
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
      'accessor': d => d['Investigative']['count'],
      Cell: row => (
          <div>{countCellHelper(row.value)}</div>
        )
    }, {
      'Header': 'Percent',
      'id': 'investigativePercent',
      'accessor': d => d['Investigative']['percent'],
      Cell: row => (
        <div>{percentCellHelper(row.value)}</div>
      )
    }]
  }, {
    Header: 'Equipment',
    columns: [{
      'Header': 'Stops',
      'id': 'equipmentCount',
      'accessor': d => d['Equipment']['count'],
      Cell: row => (
          <div>{countCellHelper(row.value)}</div>
        )
    }, {
      'Header': 'Percent',
      'id': 'equipmentCount',
      'accessor': d => d['Equipment']['percent'],
      Cell: row => (
        <div>{percentCellHelper(row.value)}</div>
      )
    }]
  }, {
    Header: 'Motor Vehicle',
    columns: [{
      'Header': 'Stops',
      'id': 'mvCount',
      'accessor': d => d['Motor Vehicle']['count'],
      Cell: row => (
          <div>{countCellHelper(row.value)}</div>
        )
    }, {
      'Header': 'Percent',
      'id': 'mvPercent',
      'accessor': d => d['Motor Vehicle']['percent'],
      Cell: row => (
        <div>{percentCellHelper(row.value)}</div>
      )
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
      'accessor': d => d['16 to 25']['count'],
      Cell: row => (
          <div>{countCellHelper(row.value)}</div>
        )
    },{
      'Header': 'Percent',
      'id': 'percent16',
      'accessor': d => d['16 to 25']['percent'],
      Cell: row => (
        <div>{percentCellHelper(row.value)}</div>
      )
    }]
  }, {
    Header: '25 to 40',
    columns: [{
      'Header': 'Stops',
      'id': 'count25',
      'accessor': d => d['25 to 40']['count'],
      Cell: row => (
          <div>{countCellHelper(row.value)}</div>
        )
    },{
      'Header': 'Stops',
      'id': 'percent25',
      'accessor': d => d['25 to 40']['percent'],
      Cell: row => (
        <div>{percentCellHelper(row.value)}</div>
      )
    }]
  }, {
    Header: '40 to 60',
    columns: [{
      'Header': 'Stops',
      'id': 'count40',
      'accessor': d => d['40 to 60']['count'],
      Cell: row => (
          <div>{countCellHelper(row.value)}</div>
        )
    },{
      'Header': 'Stops',
      'id': 'percent40',
      'accessor': d => d['40 to 60']['percent'],
      Cell: row => (
        <div>{percentCellHelper(row.value)}</div>
      )
    }]
  }, {
    Header: '60+',
    columns: [{
      'Header': 'Stops',
      'id': 'count60',
      'accessor': d => d['60+']['count'],
      Cell: row => (
          <div>{countCellHelper(row.value)}</div>
        )
    },{
      'Header': 'Stops',
      'id': 'percent60',
      'accessor': d => d['60+']['percent'],
      Cell: row => (
        <div>{percentCellHelper(row.value)}</div>
      )
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
      'accessor': d => d['UAR']['count'],
      Cell: row => (
          <div>{countCellHelper(row.value)}</div>
        )
    },{
      'Header': 'Percent',
      'id': 'percentUAR',
      'accessor': d => d['UAR']['percent'],
      Cell: row => (
        <div>{percentCellHelper(row.value)}</div>
      )
    }]
  }, {
    Header: 'Mis. Summons',
    columns: [{
      'Header': 'Stops',
      'id': 'countSum',
      'accessor': d => d['Mis. Summons']['count'],
      Cell: row => (
          <div>{countCellHelper(row.value)}</div>
        )
    },{
      'Header': 'Percent',
      'id': 'percentSum',
      'accessor': d => d['Mis. Summons']['percent'],
      Cell: row => (
        <div>{percentCellHelper(row.value)}</div>
      )
    }]
  }, {
    Header: 'Infraction',
    columns: [{
      'Header': 'Stops',
      'id': 'countInf',
      'accessor': d => d['Infraction']['count'],
      Cell: row => (
          <div>{countCellHelper(row.value)}</div>
        )
    },{
      'Header': 'Percent',
      'id': 'percentInf',
      'accessor': d => d['Infraction']['percent'],
      Cell: row => (
        <div>{percentCellHelper(row.value)}</div>
      )
    }]
  }, {
    Header: 'Written Warning',
    columns: [{
      'Header': 'Stops',
      'id': 'countWarn',
      'accessor': d => d['Written Warning']['count'],
      Cell: row => (
          <div>{countCellHelper(row.value)}</div>
        )
    },{
      'Header': 'Percent',
      'id': 'percentWarn',
      'accessor': d => d['Written Warning']['percent'],
      Cell: row => (
        <div>{percentCellHelper(row.value)}</div>
      )
    }]
  },  {
    Header: 'Verbal Warning',
    columns: [{
      'Header': 'Stops',
      'id': 'countVWarn',
      'accessor': d => d['Verbal Warning']['count'],
      Cell: row => (
          <div>{countCellHelper(row.value)}</div>
        )
    },{
      'Header': 'Percent',
      'id': 'percentVWarn',
      'accessor': d => d['Verbal Warning']['percent'],
      Cell: row => (
        <div>{percentCellHelper(row.value)}</div>
      )
    }]
  }];

  return makeTable(columns, data)
}


export function buildSearchInformationTable(data) {
   const column_names = ['Cars Searched', 'Consent', 'Inventory', 'Other', 'Contraband Found'];
   const columns = columnHelper(column_names);

  return makeTable(columns, data)
}

export function buildStopAuthorityTable(data) {
  const column_names = ["White Non-Hispanic", "Black Non-Hispanic", "Asian Non-Hispanic", "Hispanic",
    "Indian American / Alaskan Native Non-Hispanic", "Total"];
  const columns = simpleColumnHelper(column_names, "authority");
  return makeTable(columns, data)
}
