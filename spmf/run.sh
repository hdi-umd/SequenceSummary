#!/bin/bash
#slowList=("output/out_author-NNS-day-1_3_P0.csv" "output/out_author-NNS-day-1_2_P0.csv")
#slowList=("output/out_author-NNS-day-1_2_P0.csv" "output/out_author-NNS-day-1_3_P0.csv" "output/out_author-NNS-day-1_4_P0.csv" "output/out_author-NNS-day-1_4_P1.csv"\
#"output/out_author-NNS-day-1_5_P0.csv" "output/out_author-NNS-day-1_5_P1.csv" "output/out_author-NNS-day-1_6_P0.csv")
#slowList=("output/out_author-NNS-day-1_2_P0.csv")
for inF in /Users/yuexichen/Desktop/code/collaborative_writing/processData/processed/VMSP/*.csv
#for inF in ./input/*.csv
do
    outF="output/out_$(basename "${inF}")"
    if [ -e "${outF}" ]
    then
        echo "${outF} already exist"
    else
        if [[ "${slowList[*]}" != *"${outF}"* ]]
        then
        echo "current out file ${outF}"
        python main.py --file "${inF}" --evttype 1 --startidx 1 --format "%m/%d/%y" --sep "," --local True --grpattr "Sequence" --attr "Event" --output "${outF}"
        fi
    fi
done