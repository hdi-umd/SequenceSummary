# Event Sequence Visual Summarization Techniques

Event sequence data arises across diverse domains, from healthcare records to user clickstreams and system logs. Effectively visualizing such data remains challenging due to the volume, variety, and complexity of temporal patterns.

This repository implements three visual summarization techniques for event sequence data, which can be used for pattern discovery, anomaly detection, and sequence clustering.

- [**CoreFlow**](https://www.zcliu.org/coreflow/coreflow-eurovis17.pdf): Creates tree-structured visualizations that highlight branching patterns in event sequences, making it easy to identify the most common paths and where they diverge.

- [**SentenTree**](https://faculty.cc.gatech.edu/~stasko/papers/infovis16-sententree.pdf): Presents event sequences as directed graphs, revealing relationships between events and allowing exploration of complex event flow patterns.

- [**Sequence Synopsis**](https://lliquid.github.io/homepage/files/ss_vast17.pdf): Generates optimized visual summaries using clustering and the minimum description length principle, balancing information preservation with visual simplicity.

![Visualization Example](https://github.com/hdi-umd/SequenceSummary/blob/main/teaser.png?raw=true)

In addition to the three visual summarization techniques, this repository provides an example usage of our data model with the [SPMF](https://www.philippe-fournier-viger.com/spmf/) library - a popular, open-source data mining library specializing in pattern mining.


#### Citation

If you use this repository in your research, please cite our paper ["A Comparative Evaluation of Visual Summarization Techniques
for Event Sequences"](https://zcliu.org/papers/SeqSummarizationEval_EuroVis23.pdf), published at Eurovis 2023:

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

## Key Capabilities

- Support for different event types (point, interval, mixed)
- Flexible input formats and time representations
- Interactive web-based visualization application
- Additional features for sequence handling, such as sequence splitting and event merging
- Parameter tuning for different levels of granularity
- Performance metrics 

## Repository Structure

```
event-sequence-analytics/
├── core/                # Core classes for algorithm implementation (Cluster, Graph, Node, Pattern, QueueElements)
├── coreflow/            # CoreFlow implementation
├── datamodel/           # Data model classes for event handling (Event, Sequence)
├── sententree/          # SentenTree implementation
├── sequencesynopsis/    # Sequence Synopsis implementation (with and without LSH)
├── spmf/                # SPMF pattern mining utilities
├── utils/               # Data loading, argument parsing and processing helpers
├── visualization/       # Web-based visualization app
└── RunAll.py            # Script to run all techniques with benchmarking
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
  - spmf (for SPMF integration)
- Node.js and npm (for visualization app)
- React (for visualization components)
- Java Runtime Environment (for SPMF)

#### Optional Requirements

SPMF java library (for running pattern mining algorithms)

## Installation

```bash
# Clone the repository
git clone https://github.com/hdi-umd/SequenceSummary.git
cd SequenceSummary

# Install Python dependencies
pip install numpy pandas matplotlib memory_profiler datasketch certifi scikit-learn requests spmf

# Set up the visualization app
cd visualization/app
npm install
npm start
```

## Quick Start Guide

All the techniques assume that the input dataset is in the csv format, where each row represents an event. 

### Running the Visualization Techniques via **Command Line**

Arguments:

--file (str): Path to the input CSV file. The file may be local, or it could be downloaded from a cloud storage, like Dropbox.

--evttype (int): Event type. Use 1 for point event, 2 for interval event, 3 for mixed (both types of events are present in the dataset).

--startidx (int): Index of the start time column in case of interval event. For point events, this is the index of the time column.

--endidx (int, optional): Index of the end time column in case of interval event. Refer to [python website](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes) for more time format codes.

--format (str): Date format (e.g., "%m/%d/%y").

--sep (str): Delimiter used in the CSV file (e.g., "," for comma).

--local (bool): Whether the file is locally available.

--spmf (bool, optional): If spmf mining would be performed.

--grpattr (str): Name of the column to group the events (rows) into sequences.

--attr (str): Name of the column that contains the event type or label.

--output (str): Directory where the output files will be saved.

#### Algorithm Specific Parameter

**CoreFlow and SentenTree**

--minsup (float): Minimum support parameter for CoreFlow and SentenTree algorithm. Controls the granularity of the visual summary by defining the threshold for including events and patterns - value between 0.0 and 1.0 (representing 0% to 100% of sequences)

**Sequence Synopsis**

Sequence Synopsis uses two balancing parameters to control the trade-off between information preservation and visual simplicity:

--alpha (float): Controls the weight given to minimizing information loss.  Higher values prioritize preserving more information from the original sequences - value between 0.0 and 1.0

--lambdaVal (float):  Controls the balance between pattern count and edit operations.  Higher values favor fewer patterns in the summary - value between 0.0 and 1.0


#### CoreFlow Example
```bash
# Run CoreFlow mining on the sample dataset
python coreflow/main.py --file "Sample_Dataset.csv" --evttype 1 --startidx 0 \
  --format "%m/%d/%y" --sep "," --local True \
  --grpattr "Sequence" --attr "Event" \
  --minsup 0.5  --output "./output/" 
```

#### SentenTree Example
```bash
# Run SentenTree mining on the sample dataset
python sententree/main.py --file "Sample_Dataset.csv" --evttype 1 --startidx 0 \
  --format "%m/%d/%y" --sep "," --local True \
  --grpattr "Sequence" --attr "Event" \
  --minsup 0.5  --output "./output/"  
```

#### Sequence Synopsis Example
```bash
# Run Sequence Synopsis mining on the sample dataset
python sequencesynopsis/main.py --file "Sample_Dataset.csv" --evttype 1 --startidx 0 \
  --format "%m/%d/%y" --sep "," --local True \
  --grpattr "Sequence" --attr "Event" \
  --alpha 0.1 --lambdaVal 0.9 --output "./output/"
```

#### Running SPMF 

Download the SPMF JAR file (spmf.jar) from the [official website](https://www.philippe-fournier-viger.com/spmf/index.php?link=download.php)


Place the JAR file in a directory of your choice (for example, in the spmf directory of the project)

```bash
cd spmf
python main.py --file "../Sample_Dataset.csv" --evttype 1 --startidx 0 --format "%m/%d/%Y" --sep "," --local True --attr "Event"
```

#### Running All Techniques for Comparison

```bash
# Run all three techniques with varying granularity levels
python RunAll.py --file "Sample_Dataset.csv" --evttype 1 --startidx 0 \
  --format "%m/%d/%y" --sep "," --local True \
  --grpattr "Sequence" --attr "Event" \
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
## Additional Features

The repository includes several data processing capabilities that enhance the analysis of event sequence data:

### Sequence Splitting (--split)

The sequence splitting feature allows breaking down long sequences into shorter ones based on temporal units:

- **Usage**: `--split [time_unit]`
- **Valid time units**: "hour", "day", "week", "month", "quarter", "year"
- **Function**: Divides sequences based on the specified time unit
- **Benefits**:
  - Facilitates pattern discovery within specific temporal segments
  - Useful for seasonal or periodic pattern analysis

Example:
```bash
python coreflow/main.py --file "Sample_Dataset.csv" --grpattr "Sequence" --attr "Event"   --split "month"
```

### Event Merging (--merge)
The event merging feature allows aggregating similar events to reduce the variety of event types and simplify analysis:

- **Usage**: `--merge [method] with --mergefile [mapping_file]`

- **Methods**:
   1. Dictionary-based merging - directly maps original event names to merged names
   2. Regex-based merging - uses regular expressions to identify patterns for merging


- **Function**: Consolidates events based on defined rules, reducing the number of unique event types
- **Benefits**:
  - Reduces visual clutter by combining semantically similar events
  - Aids in finding higher-level patterns that might be obscured by too many event types
  - Allows domain experts to encode knowledge about event similarity


The merging rules are defined in a mapping file (commonly named "dict.txt"):

**For dictionary mapping**: Odd lines contain original event names, even lines contain target merged names

**For regex mapping**: First line contains the regular expression pattern, second line contains the target merged name

Example:
```bash
python coreflow/main.py --file "Sample_Dataset.csv" --grpattr "Sequence" --attr "Event" --merge 1 --mergefile "dict.txt"
```

These features can be combined with the main visualization techniques and parameters to create customized and insightful visual summaries of event sequence data.

### Benchmarking

The repository includes built-in benchmarking functionality to evaluate and compare the performance of different pattern mining techniques:

#### Performance Metrics

The **RunAll.py** script automatically collects and logs the following performance metrics:

- **Execution Time**: Measured in seconds, showing how long each algorithm takes to process the dataset
- **Memory Usage**: Peak memory consumption during execution, measured in MB

Running the RunAll.py script will:
  1. Process the input dataset with CoreFlow, SentenTree, and Sequence Synopsis
  2. Test multiple granularity levels (minimum support values from 0.05 to 0.30)
  3. Record execution time and memory usage for each configuration
  4. Save visual summary outputs for all configurations
  5. Generate a CSV file (TimeMemoryAnalysis.csv) with detailed performance metrics



## Visualization App

The repository includes a web-based visualization application that renders the outputs from all three techniques:

```bash
cd visualization/app
npm install
npm run start
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

If you have any questions or suggestions, please open an issue.
