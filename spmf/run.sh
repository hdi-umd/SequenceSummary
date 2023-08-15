#!/bin/bash
#slowList=("output/out_author-NNS-day-1_3_P0.csv" "output/out_author-NNS-day-1_2_P0.csv")
slowList=()
for inF in /Users/yuexichen/Desktop/code/collaborative_writing/processData/processed/VMSP/*.csv
do
    outF="output/out_$(basename "${inF}")"
    echo ${outF}
    if [[ "${slowList[*]}" != *"${outF}"* ]]
    then
        python main.py --file "${inF}" --evttype 1 --startidx 1 --format "%m/%d/%y" --sep "," --local True --grpattr "Sequence" --attr "Event" --output "${outF}"
    fi
done