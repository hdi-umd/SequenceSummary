import * as atlas from "atlas-vis";

export async function renderCoreFlow(dataPath, renderer) {
  let scene = atlas.scene();
  console.log(dataPath);
  let data = await atlas.treejson(dataPath);
  console.log(data);
  // let data = "../../../datasets/Outputs/AAAsample_ed2coreflow_result.json"
  let node = scene.mark("text", { x: 120, y: 120, fontSize: "14px" });
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

export async function renderSententree(dataPath, renderer) {
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

export async function renderSeqSynopsis(dataPath, renderer) {
  let scn = atlas.scene();
  let data = await atlas.graphjson(dataPath);
  let bg = scn.mark("rect", {fillColor: "#C8E6FA", left: 100, top: 100, width: 20, strokeWidth: 0});
  scn.repeat(bg, data.nodeTable, {field: "pattern"});
  let evtBg = scn.mark("rect", {left: 200, top: 100, width: 40, height: 1, strokeColor: "#006594"}), 
      evtNm = scn.mark("text", {x: 200, y: 100}),
      evtCnt = scn.mark("text", {x: 200, y: 100, fillColor: "#006594", fontSize: "12px", fontWeight: "bold"});
  let glyph = scn.glyph(evtBg, evtNm, evtCnt);
  scn.repeat(glyph, data.nodeTable);
  scn.encode(evtNm, {channel: "text", field: "event_attribute"});
  scn.encode(evtCnt, {channel: "text", field: "value_event"});
  scn.encode(bg, {channel: "width", field: "value", aggregator: "max", rangeExtent: 40});
  scn.encode(evtBg, {channel: "width", field: "value_event", rangeExtent: 40});
  let xEnc = scn.encode(evtBg, {channel: "x", field: "pattern", rangeExtent: 400});
  let yEnc = scn.encode(glyph, {channel: "y", field: "average_index", rangeExtent: 450, invertScale: true});
  scn.find([{field: "event_attribute", values: ["_Start", "_Exit"]}, {type: "glyph"}]).forEach(d => d.visibility = "hidden");
  scn.affix(evtNm, evtBg, "x", {itemAnchor: "right", baseAnchor: "left", offset: -5});
  scn.affix(evtNm, evtBg, "y");
  scn.affix(evtCnt, evtBg, "x", {itemAnchor: "left", baseAnchor: "right", offset: 5});
  scn.affix(evtCnt, evtBg, "y");
  scn.encode(bg, {channel: "x", field: "pattern", scale: xEnc.scale});
  scn.encode(bg.topSegment, {channel: "y", field: "average_index", aggregator: "min", scale: yEnc.scale});
  scn.encode(bg.bottomSegment, {channel: "y", field: "average_index", aggregator: "max", scale: yEnc.scale});
  renderer.clear();
  renderer.render(scn);
}