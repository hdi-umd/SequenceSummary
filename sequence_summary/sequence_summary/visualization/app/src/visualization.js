import "bootstrap";
import "bootstrap/dist/css/bootstrap.css";
import "bootstrap/dist/js/bootstrap.js";
import * as atlas from "mascot-vis"
import { renderCoreFlow, renderSententree, renderSententree2, renderSeqSynopsis } from "./renderAtlas";
import React, { useEffect, useState } from "react";

function RenderVisualization(props) {
  const [isLoading, setIsLoading] = useState(true);

  console.log(props);
  useEffect(() => {
    const renderVisualizations = async () => {
      setIsLoading(true);
      try {
        // Wait for DOM elements to be ready
        await new Promise(resolve => setTimeout(resolve, 900));
    // const svgRendererCoreflow = atlas.renderer("svg", "svgElementCoreflow");
    // const svgElements = document.querySelectorAll('.svgmined');
    // svgElements.forEach(svg => {
    //   svg.setAttribute('width', '400px');
    //   svg.setAttribute('height', '600px');
    // });

    const svgRendererSentenTree = atlas.renderer("svg", "svgElementSentenTree");
    // const svgRendererSentenTree2 = atlas.renderer("svg", "svgElementSentenTree2");
    const svgRendererSeqSynopsis = atlas.renderer("svg", "svgElementSeqSynopsis");
    const svgRendererCoreflow = atlas.renderer("svg", "svgElementCoreflow");

    
    // Initialize SVG dimensions
    
    // Validate data before rendering
    if (props.coreflowJson && document.getElementById("svgElementCoreflow")) {
      await renderCoreFlow(props.coreflowJson, svgRendererCoreflow);
    }
    if (props.sententreeJson && document.getElementById("svgElementSentenTree")) {
      await renderSententree(props.sententreeJson, svgRendererSentenTree);
    }

    if (props.seqsynopsisJson && document.getElementById("svgElementSeqSynopsis")) {
      await renderSeqSynopsis(props.seqsynopsisJson, svgRendererSeqSynopsis);
    }

  } catch (error) {
    console.error("Error rendering visualizations:", error);
  } finally {
    setIsLoading(false);
  }
};

renderVisualizations();
},[props.sententreeJson, props.seqsynopsisJson, props.coreflowJson]);
  return (
    <div>
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
