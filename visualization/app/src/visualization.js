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
    <div class="vis-container">
      <div>
        <svg id="svgElementCoreflow" class="svgmined">
          {" "}
        </svg>
      </div>
      <div>
        <svg id="svgElementSentenTree" class="svgmined">
          {" "}
        </svg>
      </div>
    </div>
  );
}

export default RenderVisualization;
