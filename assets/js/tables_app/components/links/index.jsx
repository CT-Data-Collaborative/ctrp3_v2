import React from 'react';
import Checkbox from '../checkbox'

class Links extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      selectedCheckboxes: []
    };
    this.toggleCheckbox = this.toggleCheckbox.bind(this);
  }

   toggleCheckbox(label) {

    const selectedCheckboxes = this.state.selectedCheckboxes.slice();
    let pos = selectedCheckboxes.indexOf(label);
    if (pos > -1) {
      selectedCheckboxes.splice(pos, 1);
    } else {
      selectedCheckboxes.push(label);
    }

    this.setState({ selectedCheckboxes });
    this.props.updateAnalyses(selectedCheckboxes);
  };

  createCheckbox(label) {
    return (
      <Checkbox
        label={label}
        handleCheckboxChange={this.toggleCheckbox}
        key={label}
      />);
  }

  createCheckboxes() {
    return Object.keys(this.props.apiLinks).map((l) => this.createCheckbox(l))
  }

  render() {
    return (
      <div>
        <h5>Select Data View</h5>
        {this.createCheckboxes()}
      </div>
    );
  }
}

export default Links;
