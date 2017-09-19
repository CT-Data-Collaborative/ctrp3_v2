import React from 'react';

class Checkbox extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      isChecked: false,
    }
    this.toggleCheckboxChange = this.toggleCheckboxChange.bind(this);
  }


  toggleCheckboxChange() {
    const isChecked = this.state.isChecked;
    this.setState({ isChecked: !isChecked })
    this.props.handleCheckboxChange(this.props.label);
  }

  render() {
    const { label } = this.props;
    const { isChecked } = this.state;

    return (
      <div className="checkbox">
        <label>
          <input
            type="checkbox"
            value={label}
            checked={isChecked}
            onChange={this.toggleCheckboxChange}
          /> {label}
        </label>
      </div>
    );
  }
}

export default Checkbox;
