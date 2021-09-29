import "bootstrap";
import "bootstrap/dist/css/bootstrap.css";
import "bootstrap/dist/js/bootstrap.js";
import React from "react";
import { Dropdown, DropdownButton } from "react-bootstrap";

//var fileSystem = require("file-system")

const path = require("path");
// const fs = require("fs");

function DropdownDataset() {
  // function importAll(r) {
  //   return r.keys().map(r);
  // }
  // console.log(path.join(__dirname,"../../../"));
  // console.log(path.resolve('../../../../../'));
  // console.log(path.isAbsolute(__dirname));
  // console.log(path.join(__dirname,"../../../"));
  console.log(__dirname);
  const fileList = require.context("../../../datasets/Outputs", true);
  fileList.keys().forEach((key) => console.log(key));
  console.log(typeof fileList.keys()[0]);
  //Load json files
  var dataList = [];
  var dataListCoreFlow = [];
  var dataListSententree = [];

  for (let file in fileList.keys()) {
    dataList.push(
      require("../../../datasets/Outputs" + fileList.keys()[file].substring(1))
    );
  }

  // const data = require("../../../datasets/Outputs" +
  //   fileList.keys()[0].substring(1));
  console.log(dataList);

  //joining path of directory
  //const directoryPath = path.join(__dirname, "Documents");
  //passsing directoryPath and callback function
  // listReactFiles(__dirname).then(files => console.log(files))

  // fs.recurse('./', ['*.*'],
  //   function(filepath, relative, filename) {
  //   if (filename) {
  //  console.log("FILE"+filename);
  //   } else {
  //   console.log("FOLDER"+filepath);

  //   }
  // });
  // let directoryPath = "/home/zinat/Documents/Research/code/datasets/Outputs";
  // console.log(directoryPath);
  // fs.readdir(directoryPath, function (err, files) {
  //   //handling error
  //   if (err) {
  //     return console.log("Unable to scan directory: " + err);
  //   }
  //   //listing all files using forEach
  //   files.forEach(function (file) {
  //     // Do whatever you want to do with the file
  //     console.log(file);
  //   });
  // });
  return (
    <DropdownButton id="dropdown-basic-button" title="Dropdown button">
      <Dropdown.Item href="#/action-1">Action</Dropdown.Item>
      <Dropdown.Item href="#/action-2">Another action</Dropdown.Item>
      <Dropdown.Item href="#/action-3">Something else</Dropdown.Item>
    </DropdownButton>
  );
}

export default DropdownDataset;
