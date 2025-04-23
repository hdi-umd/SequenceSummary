# Event Sequence Summary Visualizations

The repository contains the codebase for the paper titled ["A Comparative Evaluation of Visual Summarization Techniques
for Event Sequences"](https://zcliu.org/papers/SeqSummarizationEval_EuroVis23.pdf), published in Eurovis, 2023.  

#### Citation

If you use this repository in your research, please cite our paper:

```bibtex
@article{https://doi.org/10.1111/cgf.14821,
author = {Zinat, Kazi Tasnim and Yang, Jinhua and Gandhi, Arjun and Mitra, Nistha and Liu, Zhicheng},
title = {A Comparative Evaluation of Visual Summarization Techniques for Event Sequences},
journal = {Computer Graphics Forum},
volume = {42},
number = {3},
pages = {173-185},
doi = {https://doi.org/10.1111/cgf.14821},
url = {https://onlinelibrary.wiley.com/doi/abs/10.1111/cgf.14821},
eprint = {https://onlinelibrary.wiley.com/doi/pdf/10.1111/cgf.14821},
year = {2023}
}
```


## Introduction

Event sequence data appears in many domains, from healthcare records to user clickstreams to system logs. Visualizing this data effectively is challenging due to the volume, variety, and complexity of temporal patterns. 

This repository implements three visualization techniques from academic literature that help users explore and understand event sequence data through different visual representations.
Each technique offers different strengths for pattern discovery, anomaly detection, and sequence clustering tasks.


![Visualization Example](https://github.com/hdi-umd/SequenceSummary/blob/main/teaser.png?raw=true)


## Features

### Visualization Techniques

- [**CoreFlow**](https://www.zcliu.org/coreflow/coreflow-eurovis17.pdf): Creates tree-structured visualizations that highlight branching patterns in event sequences, making it easy to identify the most common paths and where they diverge.

- [**SentenTree**](https://faculty.cc.gatech.edu/~stasko/papers/infovis16-sententree.pdf): Presents event sequences as directed graphs, revealing relationships between events and allowing exploration of complex event flow patterns.

- [**Sequence Synopsis**](https://lliquid.github.io/homepage/files/ss_vast17.pdf): Generates optimized visual summaries using clustering and the minimum description length principle, balancing information preservation with visual simplicity.

### Key Capabilities

- Support for different event types (point, interval, mixed)
- Flexible input formats and time representations
- Interactive web-based visualization application
- Parameter tuning for different levels of granularity
- Performance metrics 

## Repository Structure

```
event-sequence-analytics/
├── coreflow/           # CoreFlow implementation
├── sententree/         # SentenTree implementation  
├── sequencesynopsis/   # Sequence Synopsis implementation
├── spmf/               # SPMF pattern mining utilities
├── data_model/         # Core data model classes
├── visualization/      # Web-based visualization application
├── docs/               # Additional documentation
└── Event.py, EventStore.py, etc.  # Core classes for event handling
```

## Requirements

- Python 3.7+
- Required Python packages:
  - numpy
  - pandas
  - matplotlib
  - certifi
  - datasketch (for LSH implementation in Sequence Synopsis)
  - memory_profiler (for performance analysis)
- Node.js and npm (for visualization app)
- React (for visualization components)

#### Optional Requirements

SPMF java library (for running pattern mining algorithms)

## Installation

```bash
# Clone the repository
git clone https://github.com/hdi-umd/SequenceSummary.git
cd SequenceSummary

# Install Python dependencies
pip install numpy pandas matplotlib memory_profiler datasketch certifi

# Set up the visualization app
cd visualization/app
npm install
npm start
```

## Quick Start Guide

### Running the Visualization Techniques via **Command Line**

#### CoreFlow Example
```bash
# Run CoreFlow mining on the sample dataset
python coreflow/main.py --file "Sample_Dataset.csv" --evttype 1 --startidx 0 \
  --format "%m/%d/%y" --sep "," --local True \
  --grpattr "group_attribute" --attr "event_attribute" \
  --output "./output/"
```

#### SentenTree Example
```bash
# Run SentenTree mining on the sample dataset
python sententree/main.py --file "Sample_Dataset.csv" --evttype 1 --startidx 0 \
  --format "%m/%d/%y" --sep "," --local True \
  --grpattr "group_attribute" --attr "event_attribute" \
  --output "./output/"
```

#### Sequence Synopsis Example
```bash
# Run Sequence Synopsis mining on the sample dataset
python sequencesynopsis/main.py --file "Sample_Dataset.csv" --evttype 1 --startidx 0 \
  --format "%m/%d/%y" --sep "," --local True \
  --grpattr "group_attribute" --attr "event_attribute" \
  --alpha 0.1 --lambdaVal 0.9 --output "./output/"
```

#### Running All Techniques for Comparison

```bash
# Run all three techniques with varying granularity levels
python RunAll.py --file "Sample_Dataset.csv" --evttype 1 --startidx 0 \
  --format "%m/%d/%y" --sep "," --local True \
  --grpattr "group_attribute" --attr "event_attribute" \
  --output "./output/"
```

### Running the Visualization Techniques using **Python API:**

### Loading Data

All three techniques use the same data loading approach:

```python
from EventStore import EventStore

# Create event store
eventStore = EventStore()

# Import point events from CSV
eventStore.importPointEvents(
    "your_dataset.csv",     # File path
    timeStampColumnIdx=0,   # Index of timestamp column
    timeFormat="%m/%d/%y",  # Format of timestamp
    sep=",",                # Separator in CSV
    local=True              # True if file is local, False if URL
)

# Generate sequences grouped by a specific attribute
sequences = eventStore.generateSequence("group_attribute")
```

#### CoreFlow Example

```python
from coreflow.CoreFlowMiner import CoreFlowMiner

# Initialize CoreFlow with minimum/maximum support parameters
cfm = CoreFlowMiner(
    "event_attribute",                  # Attribute to analyze
    minSup=0.2 * len(sequences),        # Minimum support threshold
    maxSup=len(sequences)               # Maximum support threshold
)

# Run CoreFlow mining
root, graph = cfm.runCoreFlowMiner(sequences)

# Export visualization data
import json
with open('coreflow_result.json', 'w') as f:
    json.dump(root, f, default=lambda o: o.__dict__ if hasattr(o, "__dict__") else str(o))
```

#### SentenTree Example

```python
from sententree.SentenTreeMiner import SentenTreeMiner

# Initialize SentenTree with minimum/maximum support parameters
stm = SentenTreeMiner(
    "event_attribute",                  # Attribute to analyze
    minSup=0.2 * len(sequences),        # Minimum support threshold
    maxSup=len(sequences)               # Maximum support threshold
)

# Run SentenTree mining
graph = stm.runSentenTreeMiner(sequences)

# Export visualization data
import json
with open('sententree_result.json', 'w') as f:
    json.dump(graph, f, default=lambda o: o.__dict__ if hasattr(o, "__dict__") else str(o))
```


#### Sequence Synopsis Example

```python
from sequencesynopsis.SequenceSynopsisMinerWithWeightedLSH import SequenceSynopsisMiner

# Initialize Sequence Synopsis with balancing parameters
ssm = SequenceSynopsisMiner(
    "event_attribute",          # Attribute to analyze
    eventStore,                 # Event store containing the data
    alpha=0.1,                  # Balance between info loss and visual complexity
    lambdaVal=0.9               # Balance between pattern count and edit operations
)

# Run Sequence Synopsis mining
clusters, graph = ssm.minDL(sequences)

# Export visualization data
import json
with open('seqsynopsis_result.json', 'w') as f:
    json.dump(graph, f, default=lambda o: o.__dict__ if hasattr(o, "__dict__") else str(o))
```


## Visualization App

The repository includes a web-based visualization application that renders the outputs from all three techniques:

```bash
cd visualization/app
npm start
```

This will start a local server at http://localhost:3000 where you can:
- Select different datasets
- Adjust granularity parameters
- Compare visualization techniques side-by-side


## Performance Considerations

Each technique has different strengths and computational characteristics:

- **CoreFlow**: Fastest technique, provides the simplest visualization structure, but may miss some patterns due to greedy algorithm approach
- **SentenTree**: Offers a good balance between quality and interpretability
- **Sequence Synopsis**: Most computationally intensive and requires more time to understand, but produces highest quality summaries according to our comparative evaluation



## Related Research Papers

This implementation is based on the following papers:


- **CoreFlow**: Liu, Z., Kerr, B., Dontcheva, M., Grover, J., Hoffman, M., & Wilson, A. (2017). CoreFlow: Extracting and Visualizing Branching Patterns from Event Sequences. Computer Graphics Forum (EuroVis '17).

- **SentenTree**: Hu, M., Wongsuphasawat, K., & Stasko, J. (2016). Visualizing Social Media Content with SentenTree. IEEE Transactions on Visualization and Computer Graphics (InfoVis '16).

- **Sequence Synopsis**: Chen, Y., Xu, P., & Ren, L. (2018). Sequence Synopsis: Optimize Visual Summary of Temporal Event Data. IEEE Transactions on Visualization and Computer Graphics (VAST '17).


## Contact

For questions or suggestions, please open an issue