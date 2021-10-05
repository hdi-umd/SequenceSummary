import DropdownDataset from "./dropdownDataset";
import RenderVisualization from "./visualization";
import React, { useState } from "react";
import "./App.css";

const cf = "coreflow", st = "sententree";

function loadData() {
  let dataMap = {};
  const fileList = require.context("../public/assets", false, /\.json$/);
  
  let re = new RegExp('\\+(coreflow|sententree).*')
  //Load json files
  //TO_DO: Further nest the dictionary to have the format Dataset:Coreflow/SentenTree:File
  for (let file of fileList.keys()) {
    //let key = file.substring(2, 11);
    console.log(typeof file);
    console.log(file.search(re));
    let key = file.substring(2,).replace(re, "");
    console.log(key);
    console.log(file);
    dataMap[key] = dataMap[key] || {}; //initialize if not exists
    let minSup = file.substring(file.indexOf("_msp") + "+_msp".length);
    minSup = minSup.substring(0, minSup.indexOf(".json"));
    console.log(minSup);
    if (file.indexOf("+coreflow") >= 0) {
      dataMap[key][cf] = dataMap[key][cf] || {};
      dataMap[key][cf][minSup] = "/assets" + file.substring(1);
    };
    if (file.indexOf("+sententree") >= 0) {
      dataMap[key][st] = dataMap[key][st] || {};
      dataMap[key][st][minSup] = "/assets" + file.substring(1);
    }
    //dataMap[key].push("/assets" + file.substring(1));
    // dataMap[key].push(require("../../../datasets/Outputs" + file.substring(1)));
  }
  return dataMap;
}
function App() {
  let data = loadData();
  console.log(data);
  let defaultVal = Object.keys(data)[0];
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
      <div>
        <DropdownDataset
          dataNames={datasetNames}
          defaultValue={defaultVal}
          onSelectedValueChange={selectedValueChange}
          selectedVal={selectedValue}
        />
        <RenderVisualization
          dataSet={selectedValue}
          coreflowJson={data[selectedValue][cf][".05"]}
          sententreeJson={data[selectedValue][st][".05"]}
        />
      </div>
    </div>
  );
}

export default App;
