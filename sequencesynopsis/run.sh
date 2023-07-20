#!/bin/bash
dayLang=('3-NNS' '4-NS' '5-NNS')
metrics=('editDistance' 'Jaccard')
action='action'

for lang in "${dayLang[@]}"
do
    for metric in "${metrics[@]}"
    do
        python main.py --file "/Users/yuexichen/Desktop/code/collaborative_writing/processData/processed/${action}Df_${lang}_${metric}.csv" --evttype 1 --startidx 1 --format "%m/%d/%y" --sep "," --local True --grpattr "Sequence" --attr "Event" --fileIdentifier "${lang}_${action}_${metric}"
    done
done