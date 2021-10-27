import "bootstrap";
import "bootstrap/dist/css/bootstrap.css";
import "bootstrap/dist/js/bootstrap.js";
import * as atlas from "atlas-vis";
import { renderCoreFlow, renderSententree, renderSeqSynopsis } from "./renderAtlas";
import React from "react";

function RenderVisualization(props) {
  console.log(props);
  
  const svgRendererCoreflow = atlas.renderer("svg", "svgElementCoreflow");
  const svgRendererSentenTree = atlas.renderer("svg", "svgElementSentenTree");
  const svgRendererSeqSynopsis = atlas.renderer("svg", "svgElementSeqSynopsis");

  renderCoreFlow(props.coreflowJson, svgRendererCoreflow);
  renderSententree(props.sententreeJson, svgRendererSentenTree);
  renderSeqSynopsis(props.seqsynopsisJson, svgRendererSeqSynopsis);
  return (
    <div className="vis-container">
      <div>
        <svg id="svgElementCoreflow" className="svgmined">
          {" "}
        </svg>
        <svg id="svgElementSentenTree" className="svgmined">
          {" "}
        </svg>
        <svg id="svgElementSeqSynopsis" className="svgmined-seq-synopsis">
          {" "}
        </svg>
      </div>
    </div>
  );
}

export default RenderVisualization;
