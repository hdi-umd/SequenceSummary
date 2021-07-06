# SentenTree Implementation

The sententree implementation contains implementation of the [SentenTree Tool] (https://github.com/twitter/SentenTree) in Python

## Installation

Nothing is needed

## Input

Input has the following paramters

file: The file containing events in table format

evttpe: If the event is point, interval or mixed

startidx: Index of the start time column

endidx: Index of the end time column

format: Format time fields are given in

sep: separator of fields

local: Whether the file is locally available

attr: name of the attr to perform mining on

split: Whether to split the sequences based on any time span. e.g. week, month or year

## Example

python main.py --file "../Sample_Dataset.csv" --evttype 1 --startidx 0 --format "%m/%d/%Y" --sep "," --local True  --attr "Events" --split "day"
