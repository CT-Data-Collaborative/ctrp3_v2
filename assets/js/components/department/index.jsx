import React from 'react';
import Select from 'react-select';

class Department extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      departments: props.departments,
      department_options: props.departments[props.selectedDepartmentType],
      department_types: ['Municipal', 'State Police', 'Special'],
      selected_department_type: props.selectedDepartmentType,
      selected_department: props.selectedDepartment ? props.selectedDepartment : null,
    };
    this.selectDepartmentType = this.selectDepartmentType.bind(this);
    this.selectDepartment = this.selectDepartment.bind(this);
    this.layout = this.layout.bind(this);
  }

  selectDepartmentType(val) {
    const departments = this.state.departments;
    this.setState({
      selected_department_type: val.value,
      department_options: departments[val.value],
      selected_department: null,
     });
    this.props.selectDept(null);
  }

  selectDepartment(val) {
    this.props.selectDept(val.value);
    this.setState({ selected_department: val.value });
  }

  layout(width) {
    const deptTypes = this.state.department_types.map((d) => {
      return { value: d, label: d };
    });

    const selectedDepartmentType = this.state.selected_department_type ? this.state.selected_department_type : 'Municipal';
    const selectedDepartment = this.state.selected_department;

    const departments = this.state.department_options.map((d) => {
      return { value: d.name, label: d.name }
    });

    if (width == 'full') {
      return (
        <div className="col-sm-12">
            <h4>Location</h4>
            <hr/>
            <p>Department Type</p>
            <Select
              name="department-type-select"
              value={selectedDepartmentType}
              options={deptTypes}
              onChange={this.selectDepartmentType}
            />
            <p>Department</p>
            <Select
              name="department-select"
              value={selectedDepartment}
              options={departments}
              onChange={this.selectDepartment}
            />
        </div>
      )
    } else {
      return (
        <div className="row">
        <div className="col-md-12 ctdata-ctrp3-selector">
          <h4>Location</h4>
          <hr/>
          <p>Department Type</p>
          <Select
            name="department-type-select"
            value={selectedDepartmentType}
            options={deptTypes}
            onChange={this.selectDepartmentType}
          />
        </div>
        <div className="col-md-12 ctdata-ctrp3-selector">
          <p>Department</p>
          <Select
            name="department-select"
            value={selectedDepartment}
            options={departments}
            onChange={this.selectDepartment}
          />
        </div>
      </div>
      )
    }
  }

  render() {
    return (this.layout(this.props.width));
  }
}

export default Department;
