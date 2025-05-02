#!/bin/bash

#Sample Dataset from Coreflow Paper Test
python RunAll.py --file "datasets/coreflow_sample/Sample_Dataset.csv" --evttype 1 --startidx 1 --format "%m/%d/%y" --sep "," --local True --grpattr "Sequence" --attr "Event"
