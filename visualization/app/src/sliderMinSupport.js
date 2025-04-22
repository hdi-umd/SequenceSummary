import "bootstrap";
import "bootstrap/dist/css/bootstrap.css";
import "bootstrap/dist/js/bootstrap.js";
import React from "react";
// Using an ES6 transpiler like Babel
import ReactSlider from 'react-slider';
// To include the default styles
// import "react-slider/lib/index.css";
import "./App.css";

function SupportSlider(props) {
  // Create marks object from support labels
  // Convert marks to a list
  const marks = Object.values(props.labels).map(value => parseFloat(value));


  const handleOnChange = (value) => {
    props.onSuppportChange(value.toString());
  };

  
  return (
    <div style={{ padding: "20px" }}>
    <ReactSlider 
      className="rangeslider"
      thumbClassName="thumb"
      trackClassName="track"
      min={props.min}
      max={props.max}
      step={props.step}
      value={parseFloat(props.selectedSup)}
      orientation="horizontal"
      marks={marks}
      markClassName="mark"
      renderMark={(props) => {
        return (
          <div {...props} className="mark">
            <span>{props.key}</span>
          </div>
        );
      }}
      onChange={handleOnChange}
      renderThumb={(props, state) => <div {...props}>{state.valueNow}</div>}
    />
    <div style={{ textAlign: "center", marginTop: "10px" }}>
        Support Value: {props.selectedSup}
      </div>
    </div>
  );
}

export default SupportSlider;
