import React from 'react';
import Select from 'react-select';

class Department extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      departments: props.departments,
      department_options: props.departments['Municipal'],
      department_types: ['Municipal', 'State Police', 'Special'],
      selected_department_type: 'Municipal',
      selected_department: null,
    };
    this.selectDepartmentType = this.selectDepartmentType.bind(this);
    this.selectDepartment = this.selectDepartment.bind(this);
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

  render() {
    const deptTypes = this.state.department_types.map((d) => {
      return { value: d, label: d };
    });

    const selectedDepartmentType = this.state.selected_department_type ? this.state.selected_department_type : '';
    const selectedDepartment = this.state.selected_department;

    const departments = this.state.department_options.map((d) => {
      return { value: d.name, label: d.name }
    });

    return (
      <div>
        <h5>Department Type</h5>
        <Select
          name="department-type-select"
          value={selectedDepartmentType}
          options={deptTypes}
          onChange={this.selectDepartmentType}
        />
      <h5>Department</h5>
        <Select
          name="department-select"
          value={selectedDepartment}
          options={departments}
          onChange={this.selectDepartment}
        />
      </div>

    );
  }
}

export default Department;
