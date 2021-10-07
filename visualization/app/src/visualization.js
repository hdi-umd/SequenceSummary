import "bootstrap";
import "bootstrap/dist/css/bootstrap.css";
import "bootstrap/dist/js/bootstrap.js";
import * as atlas from "atlas-vis";
import { renderTree, renderTree2 } from "./renderAtlas";
import React from "react";

function RenderVisualization(props) {
  console.log(props);
  
  const svgRendererCoreflow = atlas.renderer("svg", "svgElementCoreflow");
  const svgRendererSentenTree = atlas.renderer("svg", "svgElementSentenTree");

  renderTree(props.coreflowJson, svgRendererCoreflow);
  renderTree2(props.sententreeJson, svgRendererSentenTree);

  return (
    <div className="vis-container">
      <div>
        <svg id="svgElementCoreflow" className="svgmined">
          {" "}
        </svg>
        <svg id="svgElementSentenTree" className="svgmined">
          {" "}
        </svg>
      </div>
    </div>
  );
}

export default RenderVisualization;
