# SequenceSynopsis Implementation

The sententree implementation contains implementation of the [SequenceSynopsis Tool](https://lliquid.github.io/homepage/files/ss_vast17.pdf) in Python

## Installation

`pip install -r requirements.txt`

## input file:
an example input file: `../coreflow_paper_test.csv`

`Event`: event names, string

`Date`: formatted date in `%m/%d/%y`

`Sequence`: the identifier of an sequence an event belongs to, number 


## how to run Sequence Synopsis

`python main.py --file "../coreflow_paper_test.csv" --evttype 1 --startidx 1 --format "%m/%d/%y" --sep "," --local True --grpattr "Sequence" --attr "Event"`

`main.py` has the following paramters:

file: The url/ path file containing events in table format. It can be a csv file, locally available, or it could be downladed from a cloud storage, like dropbox. Expected value: String.

evttpe: If the events in the dataset are point (hapenning at an specific moment), interval (happenning along a time span) or mixed (both type of events present). Expected value: Int. representation: point: 1, interval: 2, mixed: 3.

startidx: Index of the start time column in case of interval event. For point events, this is the index of the time column. Expected value: Int.

endidx: Index of the end time column in case of interval event. Should be blank for point events. Expected value: Int.

format: Format time fields are given in. Example: %m-%d-%y. Refer to [python website](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes) for more time format codes. Expected value: String.

sep: How the fields are seperated in file. Expected values: "\t", "," etc. Expected value: String.

local: Whether the file is locally available. Expected value: Boolean.

grpattr: name of the attr to group events on to generate sequences. Expected value: String.

attr: name of the attr to perform mining on. Expected value: String.

split: Whether to split the sequences based on any time span. e.g. week, month or year. Expected value: String.


## output file:
there are two example output files:
`./sequence_synopsis_outfile.csv` and a JSON version: `./sequence_synopsis_outfile.json`
The output has 4 fields: Pattern_ID, Event, Average_Index and Number of Sequences

`Average_Index` is the average position of first appearance of an event across all the sequences. For example, if there are three sequences: A-C-A, B-C and B-A-C, the average index of the first A will be (0+1)/2 = 0.5 and the `Number of Sequences` will be 2. since it appears in the first and third sequence, at positions 0 and 1 respectively.
