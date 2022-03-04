import "bootstrap";
import "bootstrap/dist/css/bootstrap.css";
import "bootstrap/dist/js/bootstrap.js";
import * as atlas from "atlas-vis";
import { renderCoreFlow, renderSententree, renderSententree2, renderSeqSynopsis } from "./renderAtlas";
import React from "react";

function RenderVisualization(props) {
  console.log(props);
  
  const svgRendererCoreflow = atlas.renderer("svg", "svgElementCoreflow");
  const svgRendererSentenTree = atlas.renderer("svg", "svgElementSentenTree");
  const svgRendererSentenTree2 = atlas.renderer("svg", "svgElementSentenTree2");
  const svgRendererSeqSynopsis = atlas.renderer("svg", "svgElementSeqSynopsis");

  renderCoreFlow(props.coreflowJson, svgRendererCoreflow);
  renderSententree(props.sententreeJson, svgRendererSentenTree);
  // renderSententree2(props.sententreeJson, svgRendererSentenTree2);
  renderSeqSynopsis(props.seqsynopsisJson, svgRendererSeqSynopsis);
  return (
    <div id>
      <svg id="svgElementSeqSynopsis" className="svgmined">
          {" "}
        </svg>
        <svg id="svgElementCoreflow" className="svgmined">
          {" "}
        </svg>
        <svg id="svgElementSentenTree" className="svgmined">
          {" "}
        </svg>
        {/* <svg id="svgElementSentenTree2" className="svgmined">
          {" "}
        </svg> */}
        
    </div>
  );
}

export default RenderVisualization;
