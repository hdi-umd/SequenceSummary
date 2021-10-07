import "bootstrap";
import "bootstrap/dist/css/bootstrap.css";
import "bootstrap/dist/js/bootstrap.js";
import React, {useState, Component} from "react";

// Using an ES6 transpiler like Babel
import Slider from 'react-rangeslider'

// To include the default styles
import 'react-rangeslider/lib/index.css'

function SupportSlider(props) {

    const [volume, setSliderVol] = useState(props.defaultSup);
    
  
    const handleOnChange = (value) => {
      
      setSliderVol(value.toFixed(2));
      console.log(volume);
    }
  
    
    return (
    <Slider
        min = {props.min}
        max = {props.max}
        step = {props.step}
        value={volume}
        orientation="horizontal"
        tooltip={true} 
        labels = {props.labels}
        onChange={handleOnChange}
    />
    )
    
  }

export default SupportSlider;