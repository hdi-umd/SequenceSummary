import DropdownDataset from "./dropdownDataset";
import RenderVisualization from "./visualization";
import React, { useState } from "react";

function loadData() {
  let dataMap = {};
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
  return dataMap;
}
function App() {
  let data = loadData();
  console.log(data);
  let defaultVal = Object.keys(data)[3];
  let datasetNames = Object.keys(data);

  const [selectedValue, setSelectedValue] = useState(defaultVal);
  const selectedValueChange = (value) => {
    // console.log(value);
    setSelectedValue(value);
    // console.log(selectedValue);
  };
  
  console.log(defaultVal);
  return (
    <div className="App">
      <DropdownDataset
        dataNames={datasetNames}
        defaultValue={datasetNames[3]}
        onSelectedValueChange={selectedValueChange}
      />
      <RenderVisualization 
        dataSet = {selectedValue}
        coreflowJson = {data[selectedValue][0]}
        sententreeJson = {data[selectedValue][1]}
      />
    </div>
  );
}

export default App;
