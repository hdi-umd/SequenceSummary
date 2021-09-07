import React from 'react';

class VizViews extends React.Component {
  render() {
    return (
      <div>
        <div id="coreflow"
        style={{height: "30vh", width: "100vw", display: "flex"}}>
        *Coreflow visualization here*
        </div>

        <div id="sententree"
        style={{height: "30vh", width: "100vw", display: "flex"}}>
        *Sententree visualization here*
        </div>

        <div id="sequence-synopsis"
        style={{height: "30vh", width: "100vw", display: "flex"}}>
        *Sequence Synopsis visualization here*
        </div>
      </div>
    );
  }
}

export default VizViews;
