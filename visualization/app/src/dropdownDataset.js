import "bootstrap";
import "bootstrap/dist/css/bootstrap.css";
import "bootstrap/dist/js/bootstrap.js";
import React, {useState} from "react";
import { Dropdown, DropdownButton} from "react-bootstrap";

function CreateSelectItems(props) {
  //console.log(props.value);
  return <Dropdown.Item eventkey={props.value}>{props.value.substring(2)}</Dropdown.Item>;
  // let items = [];
  // for (let data of dataList) {
  //     items.push(<Dropdown.Item eventkey={data} value={data}>{data}</Dropdown.Item>);
  //     //here I will be creating my options dynamically based on
  //     //what props are currently passed to the parent component
  // }
  // return items;
}

// function onDropdownSelected(eventkey, evt) {
//   //event.persist();
//   //console.log("THE VAL", eventkey);
//   console.log(evt.target);
//   console.log(evt.target.innerText);
//   setSelectedValue(evt.target.innerText);
//   //here you will see the current selected value of the select input
// }

function DropdownDataset(props) {
  const [selectedValue,setSelectedValue]=useState('');

  const onDropdownSelected=(eventkey, evt)=>{
    //event.persist();
    //console.log("THE VAL", eventkey);
    console.log(evt.target);
    console.log(evt.target.innerText);
    setSelectedValue(evt.target.innerText);
    //here you will see the current selected value of the select input
  }

  const fileList = require.context(
    "../../../datasets/Outputs",
    false,
    /\.json$/
  );
  //fileList.keys().forEach((key) => console.log(key));
  //console.log(typeof fileList.keys()[0]);
  //Load json files
  var dataMap = {};
  //TO_DO: Further nest the dictionary to have the format Dataset:Coreflow/SentenTree:File
  for (let file of fileList.keys()) {
    let key = file.substring(0, 11);
    dataMap[key] = dataMap[key] || []; //initialize if not exists
    dataMap[key].push(require("../../../datasets/Outputs" + file.substring(1)));
  }

  //console.log(dataMap);

  const listItems = fileList
    .keys()
    .map((file) => <CreateSelectItems key={file} value={file} />);

  return (
    <DropdownButton
      id="dropdown-basic-button"
      title="Dropdown button"
      onSelect={onDropdownSelected}
    >
      {listItems}
      {/* {createSelectItems(fileList.keys())} */}
    </DropdownButton>
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
