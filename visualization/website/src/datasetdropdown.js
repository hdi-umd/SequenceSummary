import 'bootstrap';
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap/dist/js/bootstrap.js';
import $ from 'jquery';
import Popper from 'popper.js';
import React from 'react';
import Dropdown from 'react-bootstrap/Dropdown';

class DatasetDropdown extends React.Component {
  render() {
    return (
      <div>
        <Dropdown>
          <Dropdown.Toggle variant="success" id="dropdown-basic">
            Dataset
          </Dropdown.Toggle>

          <Dropdown.Menu>
            <Dropdown.Item href="#">Children Hospital</Dropdown.Item>
            <Dropdown.Item href="#">Movement post emergency department</Dropdown.Item>
            <Dropdown.Item href="#">Sequence Braiding</Dropdown.Item>
            <Dropdown.Item href="#">VAST MC1 2017</Dropdown.Item>
            <Dropdown.Item href="#">UMDVsUNC</Dropdown.Item>
          </Dropdown.Menu>

        </Dropdown>
      </div>
    );
  }
}

export default DatasetDropdown;
