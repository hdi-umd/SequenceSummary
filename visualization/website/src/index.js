import ReactDOM from 'react-dom';
import './index.css';
import React from 'react';
import DatasetDropdown from './datasetdropdown.js'
import VizViews from "./vizviews.js";

ReactDOM.render(
  <div>
    <DatasetDropdown/>
    <VizViews/>
  </div>,
  document.getElementById('root')
);
