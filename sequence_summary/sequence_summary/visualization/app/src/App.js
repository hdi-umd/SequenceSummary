import DropdownDataset from "./dropdownDataset";
import RenderVisualization from "./visualization";
import SupportSlider from "./sliderMinSupport";
import React, { useState, useEffect } from 'react';
import "./App.css";

const cf = "coreflow",
  st = "sententree",
  ss = 'seqsynopsis';


function loadData() {
  let dataMap = {};
  const fileList = require.context("../public/assets", false, /\.json$/);
  let minSupValues = {};
  let filePath = "/assets";

  let re = new RegExp("\\+(coreflow|sententree|seqsynopsis).*");
  //Load json files

  try {
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

      filePath = "/assets" + file.substring(1);
      // console.log('fff', filePath);
      if (file.indexOf("+coreflow") >= 0) {
        dataMap[key][cf] = dataMap[key][cf] || {};
        dataMap[key][cf][minSup] = filePath;
      }
      else if (file.indexOf("+sententree") >= 0) {
        dataMap[key][st] = dataMap[key][st] || {};
        dataMap[key][st][minSup] = filePath;
      }
      else if (file.indexOf("+seqsynopsis") >= 0) {
        dataMap[key][ss] = dataMap[key][ss] || {};
        dataMap[key][ss][minSup] = filePath;
      }
    } 
    console.log("Data Map:", dataMap);
    console.log("Support Values:", minSupValues);

    return { dataMap: dataMap, minSup: minSupValues };
  }catch (error) {
    console.log(filePath);
    console.error("Error loading data:", error);
    
    return { dataMap: {}, minSup: {} };
    }

  
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
    setSliderValue(Number(value).toFixed(2)); // make sure it is two digits after the decimal point
    console.log(value);
  };

  console.log(defaultVal);
  const [isLoading, setIsLoading] = useState(false);
  const [jsonData, setJsonData] = useState({
    coreflow: null,
    sententree: null,
    seqsynopsis: null
  });

  useEffect(() => {
    const loadJsonData = async () => {
      setIsLoading(true);
      try {
        const [coreflowData, sententreeData, seqsynopsisData] = await Promise.all([
          fetch(data[selectedValue][cf][sliderValue]).then(res => res.json()),
          fetch(data[selectedValue][st][sliderValue]).then(res => res.json()),
          fetch(data[selectedValue][ss][sliderValue]).then(res => res.json())
        ]);

        setJsonData({
          coreflow: coreflowData,
          sententree: sententreeData,
          seqsynopsis: seqsynopsisData
        });
      } catch (error) {
        console.error("Error loading JSON data:", error);
      } finally {
        setIsLoading(false);
      }
    };

    loadJsonData();
  }, [selectedValue, sliderValue]);
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
      <div key={`${selectedValue}-${sliderValue}`}>
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
