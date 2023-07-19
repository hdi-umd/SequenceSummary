dayLang='5-NNS'
python main.py --file "/Users/yuexichen/Desktop/code/collaborative_writing/processData/processed/sequenceDf_$dayLang.csv" --evttype 1 --startidx 1 --format "%m/%d/%y" --sep "," --local True --grpattr "Sequence" --attr "Event" --fileIdentifier "$dayLang"
