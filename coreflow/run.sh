#!/bin/bash
dayLang=('1-NNS' '1-NS' '2-NS' '3-NNS' '4-NS' '5-NNS')

for lang in "${dayLang[@]}"
  do
  python main.py --file "/Users/yuexichen/Desktop/code/collaborative_writing/processData/processed/sequenceDf_${lang}.csv" --evttype 1 --startidx 1 --format "%m/%d/%y" --sep "," --local True --grpattr "Sequence" --attr "Event"
  done