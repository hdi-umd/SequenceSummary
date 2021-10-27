import "bootstrap";
import "bootstrap/dist/css/bootstrap.css";
import "bootstrap/dist/js/bootstrap.js";
import React from "react";
import { Dropdown, DropdownButton } from "react-bootstrap";

function CreateSelectItems(props) {
  //console.log(props.value);
  return <Dropdown.Item eventkey={props.value}>{props.value}</Dropdown.Item>;
}

function DropdownDataset(props) {
  console.log(props.dataNames);

  const onDropdownSelected = (eventkey, evt) => {
    //event.persist();
    // console.log(evt.target);
    // console.log(evt.target.innerText);
    props.onSelectedValueChange(evt.target.innerText);
    //console.log(dataMap[String(selectedValue)]);
  };

  const listItems = props.dataNames.map((file) => (
    <CreateSelectItems key={file} value={file} />
  ));

  return (
    <div>
      <DropdownButton variant="outline-primary"
        id="dropdown-basic-button"
        title={props.selectedVal}
        onSelect={onDropdownSelected}
      >
        {listItems}
        {/* {createSelectItems(fileList.keys())} */}
      </DropdownButton>
      {/* <h5>You selected {selectedValue}</h5> */}
      {/* <h5>You selected  {JSON.parse(dataMap[String(selectedValue)][0])}</h5> */}
    </div>
  );
}

export default DropdownDataset;
