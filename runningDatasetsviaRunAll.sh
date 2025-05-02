#!/bin/bash

#Sample Dataset from Coreflow Paper Test
python RunAll.py --file "./Sample_Dataset.csv" --evttype 1 --startidx 0 --format "%m/%d/%y" --sep "," --local True --grpattr "Sequence" --attr "Event"
