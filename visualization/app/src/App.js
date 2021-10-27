import DropdownDataset from "./dropdownDataset";
import RenderVisualization from "./visualization";
import SupportSlider from "./sliderMinSupport";
import React, { useState } from "react";
import "./App.css";

const cf = "coreflow",
  st = "sententree",
  ss = 'seqsynopsis';

function loadData() {
  let dataMap = {};
  const fileList = require.context("../public/assets", false, /\.json$/);
  let minSupValues = {};

  let re = new RegExp("\\+(coreflow|sententree|seqsynopsis).*");
  //Load json files

  for (let file of fileList.keys()) {
    let key = file.substring(2).replace(re, "");

    dataMap[key] = dataMap[key] || {}; //initialize if not exists
    let keyword = "_msp"
    if (file.indexOf(keyword) === -1){
      keyword = "_alpha"
    }
    let minSup = file.substring(file.indexOf(keyword) + keyword.length);
    minSup = minSup.substring(0, minSup.indexOf(".json"));
    if (!(minSup in minSupValues)) {
      minSupValues[minSup] = minSup;
    }
    if (file.indexOf("+coreflow") >= 0) {
      dataMap[key][cf] = dataMap[key][cf] || {};
      dataMap[key][cf][minSup] = "/assets" + file.substring(1);
    }
    else if (file.indexOf("+sententree") >= 0) {
      dataMap[key][st] = dataMap[key][st] || {};
      dataMap[key][st][minSup] = "/assets" + file.substring(1);
    }
    else if (file.indexOf("+seqsynopsis") >= 0) {
      dataMap[key][ss] = dataMap[key][ss] || {};
      dataMap[key][ss][minSup] = "/assets" + file.substring(1);
    }
  }
  console.log(minSupValues);
  return { dataMap: dataMap, minSup: minSupValues };
}
function App() {
  let dataDetails = loadData();
  let data = dataDetails["dataMap"];
  let support = dataDetails["minSup"];
  console.log(dataDetails);
  let defaultVal = Object.keys(data)[0];
  let datasetNames = Object.keys(data);
  let supportRange = Object.keys(support);
  let defaultSupport = supportRange[Math.round(supportRange.length / 2)];
  console.log(support);
  console.log(defaultSupport);

  const [selectedValue, setSelectedValue] = useState(defaultVal);
  const [sliderValue, setSliderValue] = useState(defaultSupport);
  console.log(sliderValue);

  const selectedValueChange = (value) => {
    setSelectedValue(value);
  };

  const setSliderValueChange = (value) => {
    setSliderValue(value);
    console.log(sliderValue.substring(1));
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
      </div>
      <div>
        <SupportSlider
          support={supportRange}
          defaultSup={parseFloat(defaultSupport)}
          selectedSup={sliderValue}
          onSuppportChange={setSliderValueChange}
          min={Math.min(...supportRange)}
          max={Math.max(...supportRange)}
          step={supportRange[1] - supportRange[0]}
          labels={support}
        />
      </div>
      <div>
        <RenderVisualization
          dataSet={selectedValue}
          coreflowJson={data[selectedValue][cf][sliderValue]}
          sententreeJson={data[selectedValue][st][sliderValue]}
          seqsynopsisJson={data[selectedValue][ss][sliderValue]}
        />
      </div>
    </div>
  );
}

export default App;
