import * as atlas from "atlas-vis";
import { dagStratify, decrossOpt, sugiyama } from "d3-dag";

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
  let node = scene.mark("text", { x: 100, y: 100, fontSize: "11px" });
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
    fontSize: "11px",
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
  let node = scene.mark("text", { x: 100, y: 100, fontSize: "11px" });
  let nodes = scene.repeat(node, data.nodeTable);
  scene.encode(node, {field: "event_attribute", channel: "text"});
  nodes.layout = atlas.layout("sugiyama", {top: 100, left: 100});
  scene.encode(node, {
    field: "average_index",
    channel: "y",
    rangeExtent: 400,
    invertScale: true,
  });
  scene.encode(link, { channel: "source", field: "source" });
  scene.encode(link, { channel: "target", field: "target" });
  scene.encode(link, { channel: "strokeWidth", field: "count", range: [1, 6] });
  let linkWeight = scene.mark("text", {
    fillColor: "#006594",
    fontSize: "11px",
    fontWeight: "bold"
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

export async function renderSententree2(dataPath, renderer) {
  let scene = atlas.scene();
  let graph = await atlas.graphjson(dataPath);
  //in case the node ids in the input graph file are integers
  let nodeIdHash = new Map(), nids = {}, nodeId = "id";
  for (let n of graph.nodes) {
      nodeIdHash.set(n.id, n.id + "");
      nids[n.id + ""] = [];
  }       
  for (let l of graph.links) {
      nids[l.target+""].push(l.source+"");
  }
  let data = [];
  for (let t in nids)
      data.push({"id": t, "parentIds": nids[t]});

  let wd = 575, ht = 700, left = 50, top = 100;
  const dag = dagStratify()(data);
  const layout = sugiyama().decross(decrossOpt()).size([wd, ht]);
  //.nodeSize(n => [20, 12]);
  layout(dag);
  let t = Math.min(...dag.descendants().map(d => d.y)), l = Math.min(...dag.descendants().map(d => d.x));
  let dx = left - l, dy = top - t;
  const nid2pos = {};
  for (const node of dag.descendants()) {
      nid2pos[node.data.id] = {x: node.x + dx, y: node.y + dy};
  }

  let link = scene.mark("link", {
    sourceAnchor: ["center", "bottom"],
    targetAnchor: ["center", "top"],
    sourceOffset: [0, 2],
    targetOffset: [0, -2],
    mode: "curveVertical",
    strokeColor: "#C8E6FA",
  });
  let links = scene.repeat(link, graph.linkTable);
  let node = scene.mark("text", { x: 100, y: 100, fontSize: "11px" });
  let nodes = scene.repeat(node, graph.nodeTable);
  scene.encode(node, {field: "event_attribute", channel: "text"});

  for (let node of nodes.children) {
    let nid = node.dataScope.getFieldValue(nodeId);
    node.x = nid2pos[nodeIdHash.get(nid)].x;
    node.y = nid2pos[nodeIdHash.get(nid)].y;
    console.log(node.x, node.y);
  }

  scene.encode(node, {
    field: "average_index",
    channel: "y",
    rangeExtent: 400,
    invertScale: true,
  });
  scene.encode(link, { channel: "source", field: "source" });
  scene.encode(link, { channel: "target", field: "target" });
  scene.encode(link, { channel: "strokeWidth", field: "count", range: [1, 6] });
  let linkWeight = scene.mark("text", {
    fillColor: "#006594",
    fontSize: "11px",
    fontWeight: "bold"
  });
  let lws = scene.repeat(linkWeight, graph.linkTable);
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
      let c = graph.getNode(l.dataScope.getFieldValue("target")),
          p = graph.getNode(l.dataScope.getFieldValue("source"));
      if (c["average_index"] == p["average_index"])
          l.visibility = "hidden";
  }
  for (let l of lws.children) {
      let c = graph.getNode(l.dataScope.getFieldValue("target")),
          p = graph.getNode(l.dataScope.getFieldValue("source"));
      if (c["average_index"] == p["average_index"])
          l.visibility = "hidden";
  }
  renderer.clear();
  renderer.render(scene);
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
    evtNm = scn.mark("text", { x: 200, y: 100, fontSize: "11px"}),
    evtCnt = scn.mark("text", {
      x: 200,
      y: 100,
      fillColor: "#006594",
      fontSize: "11px",
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
    rangeExtent: 400,
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
