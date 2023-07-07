# SequenceSynopsis Implementation

The sententree implementation contains implementation of the [SequenceSynopsis Tool](https://lliquid.github.io/homepage/files/ss_vast17.pdf) in Python

## Installation

`pip install -r requirements.txt`

## Input

Input has the following paramters

file: The url/ path file containing events in table format. It can be a csv file, locally available, or it could be downladed from a cloud storage, like dropbox. Expected value: String.

evttpe: If the events in the dataset are point (hapenning at an specific moment), interval (happenning along a time span) or mixed (both type of events present). Expected value: Int. representation: point- 1, interval- 2, mixed- 3.

startidx: Index of the start time column in case of interval event. For point events, this is the index of the time column. Expected value: Int.

endidx: Index of the end time column in case of interval event. Should be blank for point events. Expected value: Int.

format: Format time fields are given in. Example- %d-%M-%Y. Refer to [python website](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes) for more time format codes. Expected value: String.

sep: How the fields are seperated in file. Expected values: "\t", "," etc. Expected value: String.

local: Whether the file is locally available. Expected value: Boolean.

grpattr: name of the attr to group events on to generate sequences. Expected value: String.

attr: name of the attr to perform mining on. Expected value: String.

split: Whether to split the sequences based on any time span. e.g. week, month or year. Expected value: String.

## Example

1. python main.py --file "../corelow_paper_test.csv" --evttype 1 --startidx 1 --format "%m/%d/%y" --sep "," --local True --grpattr "Category" --attr "Event"
