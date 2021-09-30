import "bootstrap";
import "bootstrap/dist/css/bootstrap.css";
import "bootstrap/dist/js/bootstrap.js";
import React from "react";

function renderTree() {
  let scene = window.atlas.scene();
  let data = "../../../datasets/Outputs/AAAsample_ed2coreflow_result.json"
  let node = scene.mark("text", {
    x: 100,
    y: 100,
    fontSize: "14px",
    fontWeight: "bold",
  });
  let nodes = scene.repeat(node, data.nodeTable);
  scene.encode(node, { field: "event_attribute", channel: "text" });
  nodes.layout = window.atlas.layout("tidytree", { width: 500, height: 300 });
  scene.encode(node, {
    field: "average_index",
    channel: "x",
    rangeExtent: 600,
  });
  scene.axis("x", "average_index", {
    orientation: "bottom",
    pathVisible: false,
    tickVisible: false,
  });
  scene.gridlines("x", "average_index");
  let link = scene.mark("link", {
    sourceAnchor: ["right", "middle"],
    targetAnchor: ["left", "middle"],
    strokeColor: "#888",
    sourceOffset: [5, 0],
    targetOffset: [-5, 0],
    mode: "curveHorizontal",
  });
  let links = scene.repeat(link, data.linkTable);
  scene.encode(link, { channel: "source", field: "parent" });
  scene.encode(link, { channel: "target", field: "child" });
  scene.encode(link, {
    channel: "strokeWidth",
    field: "child.value",
    range: [0, 6],
  });
  //window.atlas.renderer("svg").render(scene, "svgElement");
  window.atlas.renderer("svg").render(scene, "svgElement");
}

function renderTree2(data) {
  let scene = window.atlas.scene();

  let link = scene.mark("link", {
    sourceAnchor: ["right", "middle"],
    targetAnchor: ["left", "middle"],
    sourceOffset: [5, 0],
    targetOffset: [-5, 0],
    mode: "curveHorizontal",
  });
  let links = scene.repeat(link, data.linkTable);
  let node = scene.mark("text", { x: 120, y: 120 });
  let nodes = scene.repeat(node, data.nodeTable);
  nodes.layout = window.atlas.layout("force", { x: 200, y: 300, iterations: 300 });
  scene.encode(node, {
    field: "average_index",
    channel: "x",
    rangeExtent: 900,
  });
  scene.encode(node, { field: "event_attribute", channel: "text" });
  scene.encode(link, { channel: "source", field: "source" });
  scene.encode(link, { channel: "target", field: "target" });
  scene.encode(link, { channel: "strokeWidth", field: "count", range: [0, 6] });
  let linkWeight = scene.mark("text", { fillColor: "blue" });
  scene.repeat(linkWeight, data.linkTable);
  scene.encode(linkWeight, { field: "count", channel: "text" });
  scene.affix(linkWeight, link, "x");
  scene.affix(linkWeight, link, "y");
  window.atlas.renderer("svg").render(scene, "svgElement");
}
function RenderVisualization(props) {
  console.log(props.sententreeJson);
  console.log(window.atlas);
  renderTree(props.coreflowJson);
  //renderTree2(props.sententreeJson);

  return <svg id="svgElement"></svg>;
  //return <> </>;
}
export default RenderVisualization;
