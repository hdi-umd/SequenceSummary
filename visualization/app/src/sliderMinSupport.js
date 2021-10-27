import "bootstrap";
import "bootstrap/dist/css/bootstrap.css";
import "bootstrap/dist/js/bootstrap.js";
import React from "react";
// Using an ES6 transpiler like Babel
import Slider from "react-rangeslider";
// To include the default styles
import "react-rangeslider/lib/index.css";
import "./App.css";

function SupportSlider(props) {
  const handleOnChange = (value) => {
    props.onSuppportChange(value.toFixed(2));
  };

  return (
    <Slider 
      min={props.min}
      max={props.max}
      step={props.step}
      value={parseFloat(props.selectedSup)}
      orientation="horizontal"
      tooltip={true}
      labels={props.labels}
      onChange={handleOnChange}
    />
  );
}

export default SupportSlider;
