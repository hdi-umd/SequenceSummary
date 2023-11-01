#!/bin/bash
alphaLs=(0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9)
lambdaLs=(0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9)
actionType="videoNgram"

if [ "$actionType" == "text" ]
then
    inputFile='/Users/yuexichen/Desktop/code/collaborative_writing/processData/processed/text_sequencesynopsis_input.csv'
    for alpha in "${alphaLs[@]}"
    do
        for lambdaVal in "${lambdaLs[@]}"
            do
            identifier=$(basename "${inputFile}" .csv | sed 's/video_textInput_//g')
            echo "${identifier}" "${alpha}" "${lambdaVal}"
            python main.py --file "${inputFile}" --evttype 1 --startidx 1 --format "%m/%d/%y" --sep "," --local True --grpattr "Sequence" \
            --attr "Event" --fileIdentifier "${identifier}" --lambdaVal "${alpha}" --alpha "${lambdaVal}"
            done
    done

else
    for inputFile in /Users/yuexichen/Desktop/code/collaborative_writing/processData/processed/ss_combinations/videoNgram/*.csv
    do
        identifier=$(basename "$inputFile" | sed 's/_ssInput_//g; s/\.csv//g')
        for alpha in "${alphaLs[@]}"
        do
            for lambdaVal in "${lambdaLs[@]}"
                do
                echo "${identifier}" "${alpha}" "${lambdaVal}"
                python main.py --file "${inputFile}" --evttype 1 --startidx 1 --format "%m/%d/%y" --sep "," --local True --grpattr "Sequence" \
                --attr "Event" --fileIdentifier "${identifier}" --lambdaVal "${alpha}" --alpha "${lambdaVal}"
                done
        done
    done
fi
