# CoreFlow Implementation

The coreflow implementation contains coreflow mining techniques

## Input

Input has the following paramters

file: The url/ path file containing events in table format. It can be a csv file, locally available, or it could be downladed from a cloud storage, like dropbox. Expected value: String.

evttpe: If the events in the dataset are point (hapenning at an specific moment), interval (happenning along a time span) or mixed (both type of events present). Expected value: Int. representation: point- 1, interval- 2, mixed- 3.

startidx: Index of the start time column in case of interval event. For point events, this is the index of the time column. Expected value: Int.

endidx: Index of the end time column in case of interval event. Should be blank for point events. Expected value: Int.

format: Format time fields are given in. Example- %d-%M-%Y. Refer to [python website](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes) for more time format codes. Expected value: String.

sep: How the fields are seperated in file. Expected values: "\t", "," etc. Expected value: String.

local: Whether the file is locally available. Expected value: Boolean.

spmf : If spmf mining would be performed. Expected value: Boolean.

grpattr: name of the attr to group events on to generate sequences. Expected value: String.

attr: name of the attr to perform mining on. Expected value: String.

split: Whether to split the sequences based on any time span. e.g. week, month or year. Expected value: String.

merge: merge events based on 1. a dictionary or 2. regular expressions. In regex case, the first line is the regex, the second line is the target value. In case of dictionary, the odd lines are the values currently in dictionary and the target values are the one you want to have as Events. This information should be in the `dict.txt` file.
Expected value: Integer.


## Example

python main.py --file "../corelow_paper_test.csv" --evttype 1 --startidx 1 --format "%m/%d/%y" --sep "," --local True --grpattr "Sequence" --attr "Event"
