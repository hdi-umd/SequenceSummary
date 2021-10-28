import * as atlas from "atlas-vis";

export async function renderCoreFlow(dataPath, renderer) {
  let scene = atlas.scene();
  console.log(dataPath);
  let data = await atlas.treejson(dataPath);
  console.log(data);
  // let data = "../../../datasets/Outputs/AAAsample_ed2coreflow_result.json"
  let link = scene.mark("link", {
    sourceAnchor: ["center", "bottom"],
    targetAnchor: ["center", "top"],
    strokeColor: "#C8E6FA",
    sourceOffset: [0, 5],
    targetOffset: [0, -5],
    mode: "curveVertical",
  });
  let links = scene.repeat(link, data.linkTable);
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
  scene.encode(link, { channel: "source", field: "parent" });
  scene.encode(link, { channel: "target", field: "child" });
  scene.encode(link, {
    channel: "strokeWidth",
    field: "child.value",
    range: [1, 6],
  });
  let lbl = scene.mark("text", {
    x: 100,
    y: 100,
    fontSize: "14px",
    fontWeight: "bold",
    fillColor: "#006594",
  });
  let lbls = scene.repeat(lbl, data.linkTable);
  scene.encode(lbl, { field: "child.value", channel: "text" });
  scene.affix(lbl, link, "x");
  scene.affix(lbl, link, "y");
  scene
    .find([
      { field: "event_attribute", values: ["_Start", "_Exit"] },
      { type: "pointText" },
    ])
    .forEach((d) => (d.visibility = "hidden"));
    for (let l of lbls.children) {
      for (let n of nodes.children) {
          if (l.bounds.overlap(n.bounds)) {
              l.visibility = "hidden";
              break;
          }
      }        
  }
  for (let l of links.children) {
      let c = data.getNode(l.dataScope.getFieldValue("child")),
          p = data.getNode(l.dataScope.getFieldValue("parent"));
      if (c["average_index"] == p["average_index"])
          l.visibility = "hidden";
  }
  for (let l of lbls.children) {
      let c = data.getNode(l.dataScope.getFieldValue("child")),
          p = data.getNode(l.dataScope.getFieldValue("parent"));
      if (c["average_index"] == p["average_index"])
          l.visibility = "hidden";
  }
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
    sourceOffset: [0, 2],
    targetOffset: [0, -2],
    mode: "curveVertical",
    strokeColor: "#C8E6FA",
  });
  let links = scene.repeat(link, data.linkTable);
  let node = scene.mark("text", { x: 100, y: 100 });
  let nodes = scene.repeat(node, data.nodeTable);
  nodes.layout = atlas.layout("force", {
    x: 200,
    y: 185,
    iterations: 300,
    repulsion: 200,
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
  scene.encode(link, { channel: "strokeWidth", field: "count", range: [1, 6] });
  let linkWeight = scene.mark("text", {
    fillColor: "#006594",
    fontSize: "14px",
    fontWeight: "bold",
  });
  let lws = scene.repeat(linkWeight, data.linkTable);
  scene.encode(linkWeight, { field: "count", channel: "text" });
  scene.affix(linkWeight, link, "x");
  scene.affix(linkWeight, link, "y");
  scene
    .find([
      { field: "event_attribute", values: ["_Start", "_Exit"] },
      { type: "pointText" },
    ])
    .forEach((d) => (d.visibility = "hidden"));
  for (let l of lws.children) {
    for (let n of nodes.children) {
        if (l.bounds.overlap(n.bounds)) {
            l.visibility = "hidden";
            break;
        }
    }        
  }
  for (let l of links.children) {
      let c = data.getNode(l.dataScope.getFieldValue("target")),
          p = data.getNode(l.dataScope.getFieldValue("source"));
      if (c["average_index"] == p["average_index"])
          l.visibility = "hidden";
  }
  for (let l of lws.children) {
      let c = data.getNode(l.dataScope.getFieldValue("target")),
          p = data.getNode(l.dataScope.getFieldValue("source"));
      if (c["average_index"] == p["average_index"])
          l.visibility = "hidden";
  }
  renderer.clear();
  renderer.render(scene);
  //atlas.renderer("svg","svgElement").render(scene, "svgElement");
}

export async function renderSeqSynopsis(dataPath, renderer) {
  let scn = atlas.scene();
  let data = await atlas.graphjson(dataPath);
  let bg = scn.mark("rect", {
    fillColor: "#C8E6FA",
    left: 100,
    top: 100,
    width: 1,
    strokeWidth: 0,
  });
  scn.repeat(bg, data.nodeTable, { field: "pattern" });
  let evtBg = scn.mark("rect", {
      left: 100,
      top: 100,
      width: 1,
      height: 1,
      strokeColor: "#006594",
    }),
    evtNm = scn.mark("text", { x: 200, y: 100 }),
    evtCnt = scn.mark("text", {
      x: 200,
      y: 100,
      fillColor: "#006594",
      fontSize: "14px",
      fontWeight: "bold",
    });
  let glyph = scn.glyph(evtBg, evtNm, evtCnt);
  scn.repeat(glyph, data.nodeTable);
  scn.encode(evtNm, { channel: "text", field: "event_attribute" });
  scn.encode(evtCnt, { channel: "text", field: "value_event" });
  scn.encode(bg, {
    channel: "width",
    field: "value",
    aggregator: "max",
    rangeExtent: 6,
  });
  scn.encode(evtBg, { channel: "width", field: "value_event", rangeExtent: 6 });
  let xEnc = scn.encode(evtBg, {
    channel: "x",
    field: "pattern",
    rangeExtent: 220,
  });
  let yEnc = scn.encode(glyph, {
    channel: "y",
    field: "average_index",
    rangeExtent: 400,
    invertScale: true,
  });
  scn
    .find([
      { field: "event_attribute", values: ["_Start", "_Exit"] },
      { type: "glyph" },
    ])
    .forEach((d) => (d.visibility = "hidden"));
  scn.affix(evtNm, evtBg, "x", {
    itemAnchor: "right",
    baseAnchor: "left",
    offset: -5,
  });
  scn.affix(evtNm, evtBg, "y");
  scn.affix(evtCnt, evtBg, "x", {
    itemAnchor: "left",
    baseAnchor: "right",
    offset: 5,
  });
  scn.affix(evtCnt, evtBg, "y");
  scn.encode(bg, { channel: "x", field: "pattern", scale: xEnc.scale });
  scn.encode(bg.topSegment, {
    channel: "y",
    field: "average_index",
    aggregator: "min",
    scale: yEnc.scale,
  });
  scn.encode(bg.bottomSegment, {
    channel: "y",
    field: "average_index",
    aggregator: "max",
    scale: yEnc.scale,
  });
  renderer.clear();
  renderer.render(scn);
}
