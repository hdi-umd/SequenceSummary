"""Implements the main method that calls and executes
all modules.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json
import argparse
import csv
import time
from Node import TreeNode, GraphNode
from Sequence import Sequence
from Graph import Graph
from EventStore import EventStore
from coreflow.CoreFlowMiner import CoreFlowMiner
from sententree.SentenTreeMiner import SentenTreeMiner
from sequencesynopsis.SequenceSynopsisMiner import SequenceSynopsisMiner


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

    if not args.output:
        if args.local:
            args.output = os.path.dirname(os.path.abspath(args.file))+"/output_minsupport/"
            print(f' Output path {args.output}')
            basename = os.path.splitext(os.path.basename(args.file))[0]
    if not os.path.exists(args.output):
        os.makedirs(args.output)


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
    

    minSupParam = 0.05
    while minSupParam <= 0.3:
        cfm = CoreFlowMiner(args.attr, minSup=minSupParam *
                            len(seqList), maxSup=len(seqList))


        # cfm.run(seqList, args.attr, root, 5 * Sequence.getSeqVolume(
        #       seqList)/100.0, Sequence.getSeqVolume(seqList), [], {}, -1)
        start = time.time()
        root, graph = cfm.runCoreFlowMiner(seqList)
        end = time.time()
        print(end - start)

        print("\n\n*****Coreflow output******\n\n")

        x = json.dumps(root, ensure_ascii=False,
                       default=TreeNode.jsonSerializeDump, indent=1)
        print(x)

        with open(args.output+basename+'+coreflow_msp'+f'{minSupParam:.2f}'+'.json', 'w') \
                  as the_file:
            the_file.write(x)



        stm = SentenTreeMiner(args.attr, minSup=minSupParam *
                              len(seqList), maxSup=len(seqList))
        start = time.time()
        graph = stm.runSentenTreeMiner(seqList)
        end = time.time()
        print(end - start)
        # print("\n\n*****SentenTree output******\n\n")

        # x = json.dumps(root, ensure_ascii=False,
        #                default=GraphNode.jsonSerializeDump, indent=1)
        # print(x)

        print("\n\n*****SentenTree Graph output******\n\n")

        y = json.dumps(graph, ensure_ascii=False,
                       default=Graph.jsonSerializeDump, indent=1)
        print(y)
        # with open(args.output+'sententree_result.json', 'w') as the_file1:
        #     the_file1.write(x)

        with open(args.output+basename+'+sententree_msp'+f'{minSupParam:.2f}'+ '.json', 'w') \
                  as the_file2:
            the_file2.write(y)
        minSupParam += 0.05

    # syn = SequenceSynopsisMiner(args.attr)
    # ssm = syn.minDL(seqList)
    # print(ssm)

    # with open(args.output+basename+'sequence_synopsis_result.csv', 'w') as the_file:
    #     writer = csv.writer(the_file)
    #     writer.writerow(["Pattern_ID", "Event", "Average_Index"])
    #     for index, elem in enumerate(ssm):
    #         print(f'elemvalue {elem.index}')
    #         keyEvents = eventStore.getEventValue(args.attr, elem.pattern.keyEvts)
    #         print(f'key {keyEvents}')
    #         for ind, pos in enumerate(keyEvents):
    #             print(f'pos {pos} ind {ind}')
    #             writer.writerow(["P"+str(index), pos, elem.index[ind]])

    # #Cluster.printClustDict(G, "Event")

    # x = json.dumps([elem.jsonDefaultDump(args.attr, eventStore) for elem in ssm],
    #                ensure_ascii=False)
    # print(x)

    # with open(args.output+basename+'sequence_synopsis_outfile.json', 'w') as the_file3:
    #     the_file3.write(x)
