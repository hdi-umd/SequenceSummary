import "bootstrap";
import "bootstrap/dist/css/bootstrap.css";
import "bootstrap/dist/js/bootstrap.js";
import React, {useState, Component} from "react";

// Using an ES6 transpiler like Babel
import Slider from 'react-rangeslider'

// To include the default styles
import 'react-rangeslider/lib/index.css'

function VolumeSlider() {

    const [volume, setSliderVol] = useState(0);
    
  
    const handleOnChange = (value) => {
      setSliderVol(value);
    }
  
    
    return (
    <Slider
        min = {0.05}
        max = {0.3}
        step = {0.05}
        value={volume}
        orientation="horizontal"
        tooltip={true} 
        labels = {{0: '0', 0.15: '0.15', 0.30: '0.30'}}
        onChange={handleOnChange}
    />
    )
    
  }

export default VolumeSlider;