import "bootstrap";
import "bootstrap/dist/css/bootstrap.css";
import "bootstrap/dist/js/bootstrap.js";
import React, { useState } from "react";
import { Dropdown, DropdownButton } from "react-bootstrap";

function CreateSelectItems(props) {
  //console.log(props.value);
  return <Dropdown.Item eventkey={props.value}>{props.value}</Dropdown.Item>;
}

function DropdownDataset(props) {
  const [selectedValue, setSelectedValue] = useState("DND-Child");
  
  let dataMap = {};
  const onDropdownSelected = (eventkey, evt) => {
    //event.persist();
    //console.log("THE VAL", eventkey);
    console.log(evt.target);
    console.log(evt.target.innerText);
    setSelectedValue(evt.target.innerText);
    console.log(selectedValue);
    console.log(dataMap[String(selectedValue)]);

  };

  const fileList = require.context(
    "../../../datasets/Outputs",
    false,
    /\.json$/
  );
  //Load json files
  //TO_DO: Further nest the dictionary to have the format Dataset:Coreflow/SentenTree:File
  for (let file of fileList.keys()) {
    let key = file.substring(2, 11);
    dataMap[key] = dataMap[key] || []; //initialize if not exists
    dataMap[key].push(require("../../../datasets/Outputs" + file.substring(1)));
  }

  // for (let dataset in dataMap){  
  //   console.log(dataset);
  //   console.log(dataMap[dataset]);
  // }
  console.log(typeof selectedValue);
  const listItems = Object.keys(dataMap).map((file) => (
    <CreateSelectItems key={file} value={file} />
  ));

  return (
    <div>
      <DropdownButton
        id="dropdown-basic-button"
        title="Dropdown button"
        onSelect={onDropdownSelected}
      >
        {listItems}
        {/* {createSelectItems(fileList.keys())} */}
      </DropdownButton>
      <h5>You selected  {selectedValue}</h5>
      {/* <h5>You selected  {JSON.parse(dataMap[String(selectedValue)][0])}</h5> */}
    </div>
    //   <Input type="select" onChange={this.onDropdownSelected} label="Multiple Select" multiple>
    //      {this.createSelectItems()}
    // </Input>

    // <DropdownButton id="dropdown-basic-button" title="Dropdown button">
    //   <Dropdown.Item href="#/action-1">Action</Dropdown.Item>
    //   <Dropdown.Item href="#/action-2">Another action</Dropdown.Item>
    //   <Dropdown.Item href="#/action-3">Something else</Dropdown.Item>
    // </DropdownButton>
  );
}

export default DropdownDataset;
