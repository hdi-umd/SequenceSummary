import 'bootstrap';
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap/dist/js/bootstrap.js';
import React from 'react';
import { Dropdown, DropdownButton } from "react-bootstrap";

function DropdownDataset() {
  return (
    <DropdownButton id="dropdown-basic-button" title="Dropdown button">
    <Dropdown.Item href="#/action-1">Action</Dropdown.Item>
    <Dropdown.Item href="#/action-2">Another action</Dropdown.Item>
    <Dropdown.Item href="#/action-3">Something else</Dropdown.Item>
  </DropdownButton>
    
  );
}

export default DropdownDataset;
