# CoreFlow Implementation

The coreflow implementation contains both spmf and coreflow mining techniques

## Installation

To run smpf we need to install the [smpf-py module] (https://pypi.org/project/spmf/)  

> pip install spmf

We also need the [smpf.jar file] (http://www.philippe-fournier-viger.com/spmf/download-spmfjar.php) and place that in the same directory as coreflow.

## Input

Input has the folloing paramters

file: The file containing events in table format

evttpe: If the event is point, interval or mixed

startidx: Index of the start time column

endidx: Index of the end time column

format: Format time fields are given in

sep: separator of fields

local: Whether the file is locally available

spmf : If spmf mining would be performed

grpattr: name of the attr to group events on to generate sequences 

attr: name of the attr to perform mining on

split: Whether to split the sequences based on any time span. e.g. week, month or year

## Example

python main.py --file "../corelow_paper_test.csv" --evttype 1 --startidx 1 --format "%m/%d/%y" --sep "," --local True --grpattr "Category" --attr "Event"
