import * as atlas from "mascot-vis"
import {  decrossOpt, sugiyama } from "d3-dag";

export async function renderCoreFlow(dataPath, renderer) {
  let scene = atlas.scene();
  // console.log(dataPath);
  let data = await atlas.treeJSON(dataPath);
  // console.log(data);
  // let data = "../../../datasets/Outputs/AAAsample_ed2coreflow_result.json"
  let link = scene.mark("bezierCurve", {
    sourceAnchor: ["center", "bottom"],
    targetAnchor: ["center", "top"],
    strokeColor: "#eee",
    sourceOffset: [0, 2],
    targetOffset: [0, -2],
    orientation: "vertical",
  });
  // let links = scene.repeat(link, data.linkTable);
  let node = scene.mark("text", { x: 100, y: 100, fontSize: "12.5px", fontWeight: "bold" });
  // let nodes = scene.repeat(node, data.nodeTable);
  // let [nodes, _] = scene.repeat([node, link], data);
  let [nodes, links] = scene.repeat([node, link], data);
  scene.encode(node, { attribute: "event_attribute", channel: "text" });
  nodes.layout = atlas.layout("tidyTree", {
    width: 1250,
    height: 450,
    orientation: "vertical",
  });
  // scene.encode(node, {
  //   attribute: "average_index",
  //   channel: "y",
  //   rangeExtent: 400,
  //   flipScale: true,
  // });
  // scene.encode(link, { channel: "source", field: "parent" });
  // scene.encode(link, { channel: "target", field: "child" });
  scene.encode(link, {
    channel: "strokeWidth",
    attribute: "child.value",
    rangeExtent: 20,
    includeZero: true

  });
  let lbl = scene.mark("text", {x: 100, y: 100, fontSize: "12px", fillColor: "#222"});
  let lbls = scene.repeat(lbl, data.linkTable);
  scene.encode(lbl, { attribute: "child.value", channel: "text" });
  scene.affix(lbl, link, "x");
  scene.affix(lbl, link, "y");
  let se = scene
    .findElements([
      { attribute: "event_attribute", type: "list", value: ["_Start", "_Exit"] },
      {property: "type", type: "list", value: ["text"]}
    ])
  // se.forEach((d) => (d.visibility = "hidden"));
  //   for (let l of lbls.children) {
  //     for (let n of nodes.children) {
  //         if (l.bounds.overlap(n.bounds)) {
  //             l.visibility = "hidden";
  //             break;
  //         }
  //     }        
  // }
  // for (let l of links.children) {
  //     let c = data.getNode(l.dataScope.getFieldValue("child")),
  //         p = data.getNode(l.dataScope.getFieldValue("parent"));
  //     if (c["average_index"] == p["average_index"])
  //         l.visibility = "hidden";
  // }
  // for (let l of lbls.children) {
  //     let c = data.getNode(l.dataScope.getFieldValue("child")),
  //         p = data.getNode(l.dataScope.getFieldValue("parent"));
  //     if (c["average_index"] == p["average_index"])
  //         l.visibility = "hidden";
  // }
  renderer.clear();
  renderer.render(scene);
  //document.getElementById("svgElement").append("whatever");
}

export async function renderSententree(dataPath, renderer) {
  let scene = atlas.scene();
  let data = await atlas.graphJSON(dataPath);
  let link = scene.mark("bezierCurve", {
    sourceAnchor: ["center", "bottom"],
    targetAnchor: ["center", "top"],
    sourceOffset: [0, 2],
    targetOffset: [0, -2],
    orientation: "vertical",
    strokeColor: "#eee",
  });
  
  let node = scene.mark("text", { x: 120, y: 120, fontSize: "12.5px", fontWeight: "bold" });
  
  // console.log(node);
  // console.log(data);
  // console.log(link);
  // scene.encode(node, {
  //   field: "average_index",
  //   channel: "y",
  //   rangeExtent: 600,
  //   flipScale: true,
  // });
  // scene.encode(link, { channel: "source", field: "source" });
  // scene.encode(link, { channel: "target", field: "target" });
  
  // let links = scene.repeat(link, data.linkTable);
  let [nodes, _] = scene.repeat([node, link], data);
  scene.encode(node, { attribute: "event_attribute", channel: "text" });
  nodes.layout = atlas.layout("directedGraph", {top: 100, left: 100, edgeSep: 100});
  
  
  scene.encode(link, { channel: "strokeWidth", attribute: "count", rangeExtent: 20, includeZero: true });
  let linkWeight = scene.mark("text", {x: 100, y: 100,
    fillColor: "#006594",
    fontSize: "11px"
  });
  let lws = scene.repeat(linkWeight, data.linkTable);
  scene.encode(linkWeight, { attribute: "count", channel: "text" });
  scene.affix(linkWeight, link, "x");
  scene.affix(linkWeight, link, "y");
  
  // scene.encode(node, {attribute: "event_attribute", channel: "text"});
  
//   let scene = msc.scene();
// let data = await msc.graphJSON("/datasets/graphjson/UMDvsUNC-D2O+sententree_msp0.10.json");
// let node = scene.mark("text", {x: 120, y: 120}),
//     link = scene.mark("bezierCurve", {sourceAnchor: ["center", "bottom"], targetAnchor: ["center", "top"], sourceOffset: [0, 2], targetOffset: [0, -3], orientation: "vertical", strokeColor: "#C8E6FA"});
// let [nodes, links] = scene.repeat([node, link], data);
// scene.encode(node, {attribute: "name", channel: "text"});
// nodes.layout = msc.layout("directedGraph", {top: 100, left: 100, edgeSep: 100});
// scene.encode(link, {channel: "strokeWidth", attribute: "count", rangeExtent: 20});
// let linkWeight = scene.mark("text", {fillColor: "#006594", fontSize: "10px"});
// let lws = scene.repeat(linkWeight, data.linkTable);
// scene.encode(linkWeight, {attribute: "count", channel: "text"});
// scene.affix(linkWeight, link, "x");
// scene.affix(linkWeight, link, "y");
// msc.renderer('svg','svgElement').render(scene);
  // scene
  //   .find([
  //     { field: "event_attribute", values: ["_Start", "_Exit"] },
  //     { type: "pointText" },
  //   ])
  //   .forEach((d) => (d.visibility = "hidden"));
  // for (let l of lws.children) {
  //   for (let n of nodes.children) {
  //       if (l.bounds.overlap(n.bounds)) {
  //           l.visibility = "hidden";
  //           break;
  //       }
  //   }        
  // }
  // for (let l of links.children) {
  //     let c = data.getNode(l.dataScope.getFieldValue("target")),
  //         p = data.getNode(l.dataScope.getFieldValue("source"));
  //     if (c["average_index"] == p["average_index"])
  //         l.visibility = "hidden";
  // }
  // for (let l of lws.children) {
  //     let c = data.getNode(l.dataScope.getFieldValue("target")),
  //         p = data.getNode(l.dataScope.getFieldValue("source"));
  //     if (c["average_index"] == p["average_index"])
  //         l.visibility = "hidden";
  // }
  renderer.clear();
  renderer.render(scene);
  //atlas.renderer("svg","svgElement").render(scene, "svgElement");
}

// export async function renderSententree2(dataPath, renderer) {
//   let scene = atlas.scene();
//   let graph = await atlas.graphJSON(dataPath);
//   //in case the node ids in the input graph file are integers
//   let nodeIdHash = new Map(), nids = {}, nodeId = "id";
//   for (let n of graph.nodes) {
//       nodeIdHash.set(n.id, n.id + "");
//       nids[n.id + ""] = [];
//   }       
//   for (let l of graph.links) {
//       nids[l.target+""].push(l.source+"");
//   }
//   let data = [];
//   for (let t in nids)
//       data.push({"id": t, "parentIds": nids[t]});

//   let wd = 575, ht = 700, left = 50, top = 100;
//   // const dag = dagStratify()(data);
//   const layout = sugiyama().decross(decrossOpt()).size([wd, ht]);
//   //.nodeSize(n => [20, 12]);
//   layout(dag);
//   let t = Math.min(...dag.descendants().map(d => d.y)), l = Math.min(...dag.descendants().map(d => d.x));
//   let dx = left - l, dy = top - t;
//   const nid2pos = {};
//   for (const node of dag.descendants()) {
//       nid2pos[node.data.id] = {x: node.x + dx, y: node.y + dy};
//   }

//   let link = scene.mark("link", {
//     sourceAnchor: ["center", "bottom"],
//     targetAnchor: ["center", "top"],
//     sourceOffset: [0, 2],
//     targetOffset: [0, -2],
//     mode: "curveVertical",
//     strokeColor: "#C8E6FA",
//   });
//   let links = scene.repeat(link, graph.linkTable);
//   let node = scene.mark("text", { x: 100, y: 100, fontSize: "10px" });
//   let nodes = scene.repeat(node, graph.nodeTable);
//   scene.encode(node, {field: "event_attribute", channel: "text"});

//   for (let node of nodes.children) {
//     let nid = node.dataScope.getFieldValue(nodeId);
//     node.x = nid2pos[nodeIdHash.get(nid)].x;
//     node.y = nid2pos[nodeIdHash.get(nid)].y;
//     console.log(node.x, node.y);
//   }

//   scene.encode(node, {
//     field: "average_index",
//     channel: "y",
//     rangeExtent: 400,
//     flipScale: true,
//   });
//   scene.encode(link, { channel: "source", field: "source" });
//   scene.encode(link, { channel: "target", field: "target" });
//   scene.encode(link, { channel: "strokeWidth", field: "count", range: [1, 6] });
//   let linkWeight = scene.mark("text", {
//     fillColor: "#006594",
//     fontSize: "9px",
//     fontWeight: "bold"
//   });
//   let lws = scene.repeat(linkWeight, graph.linkTable);
//   scene.encode(linkWeight, { field: "count", channel: "text" });
//   scene.affix(linkWeight, link, "x");
//   scene.affix(linkWeight, link, "y");
//   scene
//     .find([
//       { field: "event_attribute", values: ["_Start", "_Exit"] },
//       { type: "pointText" },
//     ])
//     .forEach((d) => (d.visibility = "hidden"));
//   for (let l of lws.children) {
//     for (let n of nodes.children) {
//         if (l.bounds.overlap(n.bounds)) {
//             l.visibility = "hidden";
//             break;
//         }
//     }        
//   }
//   for (let l of links.children) {
//       let c = graph.getNode(l.dataScope.getFieldValue("target")),
//           p = graph.getNode(l.dataScope.getFieldValue("source"));
//       if (c["average_index"] == p["average_index"])
//           l.visibility = "hidden";
//   }
//   for (let l of lws.children) {
//       let c = graph.getNode(l.dataScope.getFieldValue("target")),
//           p = graph.getNode(l.dataScope.getFieldValue("source"));
//       if (c["average_index"] == p["average_index"])
//           l.visibility = "hidden";
//   }
//   renderer.clear();
//   renderer.render(scene);
// }

export async function renderSeqSynopsis(dataPath, renderer) {
  let scn = atlas.scene();
  let data = await atlas.graphJSON(dataPath);
  let bg = scn.mark("rect", {
    fillColor: "#ddd",
    left: 100,
    top: 100,
    width: 20,
    strokeWidth: 0,
    opacity: 0.2,
    //  strokeColor: "#C8E6FA"
  });
  // let clusterSize = scn.mark("text", {x: 200, y: 100, fontSize: "10px"});
  // let link = scn.mark("line", {
  //   sourceAnchor: ["right", "bottom"],
  //   targetAnchor: ["right", "top"],
  //   sourceOffset: [0, 2],
  //   targetOffset: [0, -2],
  //   orientation: "vertical",
  //   strokeColor: "#C8E6FA",
  // });
  scn.repeat(bg, data.nodeTable, { attribute: "pattern" });
  // scn.repeat(clusterSize, data.nodeTable, {attribute: "pattern"});
  
  let evtBg = scn.mark("rect", {
      left: 200,
      top: 100,
      width: 40,
      height: 11,
      strokeColor: "#eee",
    }),
    evtNm = scn.mark("text", { x: 500, y: 100, fontSize: "12px"}),
    evtCnt = scn.mark("text", {
      x: 200,
      y: 100,
      fillColor: "#006594",
      fontSize: "12px",
      fontWeight: "bold",
    });
  let glyph = scn.glyph(evtBg, evtNm, evtCnt);
  // let [nodes, _] = scn.repeat([glyph, link], data);
  // nodes.layout = atlas.layout("directedGraph", {top: 100, left: 100, edgeSep: 100});
  
  scn.repeat(glyph, data.nodeTable);
  
  scn.encode(evtNm, { channel: "text", attribute: "event_attribute" });
  scn.encode(evtCnt, { channel: "text", attribute: "value_event" });
  // let widthEnc = scn.encode(bg, {
  //   channel: "width",
  //   attribute: "value",
  //   range: [0,50], includeZero: true
  // });
  scn.encode(bg, {
    channel: "width",
    attribute: "value",
    aggregator: "min",
    rangeExtent: 40,
    includeZero: true,

  });
  scn.encode(evtBg, { channel: "width", attribute: "value_event", rangeExtent: 40, includeZero: true });
  // scn.encode(clusterSize, {channel: "text", attribute: "value", aggregator: "max"});
  let xEnc = scn.encode(evtBg, {
    channel: "x",
    attribute: "pattern",
    rangeExtent: 1000,
  });
  let yEnc = scn.encode(glyph, {
    channel: "y",
    attribute: "average_index",
    rangeExtent: 1050,
    flipScale: true,
  });
  // console.log(yEnc._scales[0].map(30));
  // let se = scn.findElements([{attribute: "event_attribute", type: "list", value: ["_Start", "_Exit"]}, {property: "type", type: "list", value: ["text"]}]);
  // se.forEach(d => console.log(d));
  // se.forEach(d => d._anchor = ["top", "right"]);

  // se.forEach(d => d.text = "x"); //["bototm", "right"]);
  

  // scn.findElements([{attribute: "label", value: "high"}, {property: "type", value: "text"}])
  // scn.findElements([{attribute: "event_attribute", value: "_Start"}, {property: "type", value: "text"}]).forEach((d) => (d.visibility = "hidden"));
  // scn.find([
  //     { field: "event_attribute", values: ["_Start", "_Exit"] },
  //     { type: "glyph" },
  //   ])
  //   .forEach((d) => (d.visibility = "hidden"));
  scn.affix(evtNm, evtBg, "x", {
    elementAnchor: "right",
    baseAnchor: "left",
    offset: -10,
  });
  scn.affix(evtNm, evtBg, "y");
  scn.affix(evtCnt, evtBg, "x", {
    elementAnchor: "left",
    baseAnchor: "right",
    offset: 10,
  });
  scn.affix(evtCnt, evtBg, "y");
  scn.encode(bg, { channel: "x", attribute: "pattern", shareScale: xEnc });
  scn.encode(evtBg, {channel: "fillColor", attribute: "event_attribute"});
  // scn.encode(clusterSize, {channel: "text", attribute: "pattern", shareScale: xEnc});
  // scn.affix(clusterSize, bg, "y", {
  //   elementAnchor: "top",
  //   baseAnchor: "bottom",
  //   offset: 20,
  // });
  // scn.affix(clusterSize, bg, "x");
  scn.encode(bg.topSegment, {
    channel: "y",
    attribute: "average_index",
    aggregator: "min",
    shareScale: yEnc,
  });
  scn.encode(bg.bottomSegment, {
    channel: "y",
    attribute: "average_index",
    aggregator: "max",
    shareScale: yEnc,
  });
  // scn.encode(link, { channel: "strokeWidth", attribute: "value_event", rangeExtent: 50 });
  // se.forEach(d => console.log(d));
  let se_start = scn.findElements([{attribute: "event_attribute", type: "list", value: ["_Start"]}, {property: "type", type: "list", value: ["text"]}]);
  se_start.forEach(d => d._y = 80);
  let se_exit = scn.findElements([{attribute: "event_attribute", type: "list", value: ["_Exit"]}, {property: "type", type: "list", value: ["text"]}]);
  // se_exit.forEach(d => d._y = 500);
  let se_rect = scn.findElements([{attribute: "event_attribute", type: "list", value: ["_Start", "_Exit"]}, {property: "type", type: "list", value: ["rect"]}]);
  se_rect.forEach(d => {
    d.visibility= "hidden";
  });
  se_exit.forEach(d => {
    d._y+= 12;
    });
  
  renderer.clear();
  renderer.render(scn);
}