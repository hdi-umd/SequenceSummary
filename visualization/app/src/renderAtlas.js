import * as atlas from "atlas-vis";

export async function renderTree(dataPath, renderer) {
  let scene = atlas.scene();
  console.log(dataPath);
  let data = await atlas.treejson(dataPath);
  console.log(data);
  // let data = "../../../datasets/Outputs/AAAsample_ed2coreflow_result.json"
  let node = scene.mark("text", { x: 100, y: 100, fontSize: "14px" });
  let nodes = scene.repeat(node, data.nodeTable);
  scene.encode(node, { field: "event_attribute", channel: "text" });
  nodes.layout = atlas.layout("tidytree", {
    width: 300,
    height: 500,
    orientation: "vertical",
  });
  scene.encode(node, {
    field: "average_index",
    channel: "y",
    rangeExtent: 400,
    invertScale: true,
  });
  let link = scene.mark("link", {
    sourceAnchor: ["center", "bottom"],
    targetAnchor: ["center", "top"],
    strokeColor: "#ddd",
    sourceOffset: [0, 5],
    targetOffset: [0, -5],
    mode: "curveVertical",
  });
  scene.repeat(link, data.linkTable);
  scene.encode(link, { channel: "source", field: "parent" });
  scene.encode(link, { channel: "target", field: "child" });
  scene.encode(link, {
    channel: "strokeWidth",
    field: "child.value",
    range: [0, 6],
  });
  let lbl = scene.mark("text", {
    x: 100,
    y: 100,
    fontSize: "14px",
    fontWeight: "bold",
    fillColor: "#006594",
  });
  scene.repeat(lbl, data.linkTable);
  console.log(data.linkTable);
  scene.encode(lbl, { field: "child.value", channel: "text" });
  scene.affix(lbl, link, "x");
  scene.affix(lbl, link, "y");

  renderer.clear();
  renderer.render(scene);
  //document.getElementById("svgElement").append("whatever");
}

export async function renderTree2(dataPath, renderer) {
  let scene = atlas.scene();
  let data = await atlas.graphjson(dataPath);
  let link = scene.mark("link", {
    sourceAnchor: ["center", "bottom"],
    targetAnchor: ["center", "top"],
    sourceOffset: [0, 5],
    targetOffset: [0, -5],
    mode: "curveVertical",
    strokeColor: "#ddd",
  });
  let links = scene.repeat(link, data.linkTable);
  let node = scene.mark("text", { x: 120, y: 120 });
  let nodes = scene.repeat(node, data.nodeTable);
  nodes.layout = atlas.layout("force", {
    x: 200,
    y: 150,
    iterations: 300,
    repulsion: 90,
    linkDistance: 10,
  });
  scene.encode(node, {
    field: "average_index",
    channel: "y",
    rangeExtent: 400,
    invertScale: true,
  });
  scene.encode(node, { field: "event_attribute", channel: "text" });
  scene.encode(link, { channel: "source", field: "source" });
  scene.encode(link, { channel: "target", field: "target" });
  scene.encode(link, { channel: "strokeWidth", field: "count", range: [0, 6] });
  let linkWeight = scene.mark("text", {
    fillColor: "#006594",
    fontSize: "14px",
    fontWeight: "bold",
  });
  scene.repeat(linkWeight, data.linkTable);
  scene.encode(linkWeight, { field: "count", channel: "text" });
  scene.affix(linkWeight, link, "x");
  scene.affix(linkWeight, link, "y");
  renderer.clear();
  renderer.render(scene);
  //atlas.renderer("svg","svgElement").render(scene, "svgElement");
}
