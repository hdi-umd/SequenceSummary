""" Implements the main method that calls and executes
SequenceSynopsis module.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import argparse
import csv
from EventStore import EventStore
from Sequence import Sequence
#from SequenceSynopsisMiner import SequenceSynopsisMiner
#from SequenceSynopsisMinerWithLSH import SequenceSynopsisMiner
from SequenceSynopsisMinerWithWeightedLSH import SequenceSynopsisMiner
if __name__ == "__main__":
    # main()

    argParser = argparse.ArgumentParser()

    argParser.add_argument("--file", help="File to read from",
                           type=str, default="sequence_braiding_refined.csv", required=False)

    argParser.add_argument("--evttype", help="1. Point 2.Interval 3.Mixed event",
                           type=int, default=1, required=False)

    argParser.add_argument("--startidx", help="Column Index of starting time",
                           type=int, default=0, required=False)

    argParser.add_argument("--endidx", help="Column Index of ending time",
                           type=int, default=1, required=False)

    argParser.add_argument("--format", help="Time format",
                           type=str, default="%m/%d/%y", required=False)

    argParser.add_argument("--sep", help="separator of fields",
                           type=str, default=",", required=False)

    argParser.add_argument("--local", help="Local availability of file",
                           type=bool, default=True, required=False)

    argParser.add_argument("--header", help="name of fields",
                           nargs='+', default="", required=False)

    argParser.add_argument("--attr", help="Attribute to run mining on",
                           type=str, required=True)

    argParser.add_argument("--grpattr", help="group the sequences based on this attribute",
                           type=str, default="")

    argParser.add_argument("--split", help="split the sequences",
                           type=str, default="")

    argParser.add_argument("--output", help="Path of output file",
                           type=str, default="")

    args = argParser.parse_args()
    print(args)

    # Eventstore creates a list of events
    eventStore = EventStore()
    if args.evttype == 1:
        eventStore.importPointEvents(args.file, args.startidx,
                                     args.format, sep=args.sep, local=args.local,
                                     header=args.header)
    elif args.evttype == 2:
        eventStore.importIntervalEvents(
            args.file, args.startidx, args.endidx, args.format, sep=args.sep,
            local=args.local, header=args.header)
    else:
        eventStore.importMixedEvents(args.file, args.startidx, args.endidx,
                                     args.format, sep=args.sep, local=args.local,
                                     header=args.header)

    # create Sequences from Eventstore
    if args.grpattr:
        seq = eventStore.generateSequence(args.grpattr)
    else:
        seq = Sequence(eventStore.events, eventStore)

    if args.split:
        seqList = Sequence.splitSequences(seq, args.split)
    else:
        if not isinstance(seq, list):
            seqList = [seq]
        else:
            seqList = seq

    syn = SequenceSynopsisMiner(args.attr, eventStore)
    ssm = syn.minDL(seqList)
    print(ssm)

    with open('sequence_synopsis_outfile.csv', 'w') as the_file:
        writer = csv.writer(the_file)
        writer.writerow(["Pattern_ID", "Event", "Average_Index", "Number of Sequences"])
        for index, elem in enumerate(ssm):
            print(f'elemvalue {elem.index}')
            writer.writerow(["P"+str(index), "_Start", 0, str(len(elem.seqList))])
            keyEvents = eventStore.getEventValue(args.attr, elem.pattern.keyEvts)
            print(f'key {keyEvents}')
            for ind, pos in enumerate(keyEvents):
                print(f'pos {pos} ind {ind}')
                writer.writerow(["P"+str(index), pos, elem.index[ind], str(len(elem.seqList))])
            trailingLen = sum(len(x.events) for x in elem.seqList)/len(elem.seqList)
            writer.writerow(["P"+str(index), "_Exit", trailingLen, str(len(elem.seqList))])




    #Cluster.printClustDict(G, "Event")

    x = json.dumps([elem.jsonDefaultDump(args.attr, eventStore) for elem in ssm],
                   ensure_ascii=False)
    print(x)

    with open('sequence_synopsis_outfile.json', 'w') as the_file:
        the_file.write(x)
