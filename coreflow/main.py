"""Implements the main method that calls and executes
Coreflow module.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Graph import Graph
from coreflow.CoreFlowMiner import CoreFlowMiner
from EventStore import EventStore
from Sequence import Sequence
from Node import TreeNode
import argparse
import json


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
                           type=str, default="./")

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

    cfm = CoreFlowMiner(args.attr, minSup=0.2 *
                        len(seqList), maxSup=len(seqList))

    # cfm.run(seqList, args.attr, root, 5 * Sequence.getSeqVolume(
    #       seqList)/100.0, Sequence.getSeqVolume(seqList), [], {}, -1)
    root, graph = cfm.runCoreFlowMiner(seqList)

    print("\n\n*****Coreflow output******\n\n")

    if not os.path.isdir(args.output):
        os.mkdir(args.output)

    x = json.dumps(root, ensure_ascii=False,
                   default=TreeNode.jsonSerializeDump, indent=1)
    print(x)

    with open(args.output+'coreflow_result.json', 'w') as the_file:
        the_file.write(x)

    y = json.dumps(graph, ensure_ascii=False,
                   default=Graph.jsonSerializeDump, indent=1)
    print(y)


    with open(args.output+'coreflow_graph.json', 'w') as the_file2:
        the_file2.write(y)
