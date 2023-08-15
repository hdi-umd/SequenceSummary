#!/bin/bash
identifiers=("author-NNS-day-1" "author-NNS-day-others" "author-NS-day-1" "author-NS-day-others")
outF="output/author-NNS-day-1.csv"
#inF="/Users/yuexichen/Desktop/code/collaborative_writing/processData/processed/ss_combinations/video_ssInput_author-NS-day-others.csv"
inF="../coreflow_paper_test.csv"
python main.py --file "${inF}" --evttype 1 --startidx 1 --format "%m/%d/%y" --sep "," --local True --grpattr "Sequence" --attr "Event" --output "${outF}"
