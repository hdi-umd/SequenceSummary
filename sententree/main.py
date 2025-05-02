"""Implements the main method that calls and executes SentenTree modules."""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from datamodel.EventStore import EventStore
from sententree.SentenTreeMiner import SentenTreeMiner
from core.Graph import Graph
from datamodel.EventAggregate import aggregateEventsRegex, aggregateEventsDict
from datamodel.Sequence import Sequence
import json
import argparse


if __name__ == "__main__":
    # main()

    argParser = argparse.ArgumentParser()
    argParser.add_argument(
        "--file",
        help="File to read from",
        type=str,
        default="../coreflow/sequence_braiding_refined.csv",
        required=False,
    )
    argParser.add_argument(
        "--evttype",
        help="1. Point 2.Interval 3.Mixed event",
        type=int,
        default=1,
        required=False,
    )
    argParser.add_argument(
        "--startidx",
        help="Column Index of starting time",
        type=int,
        default=0,
        required=False,
    )
    argParser.add_argument(
        "--endidx",
        help="Column Index of ending time",
        type=int,
        default=1,
        required=False,
    )
    argParser.add_argument(
        "--format", help="Time format", type=str, default="%m/%d/%y", required=False
    )

    argParser.add_argument(
        "--sep", help="separator of fields", type=str, default=",", required=False
    )
    argParser.add_argument(
        "--local",
        help="Local availability of file",
        type=bool,
        default=True,
        required=False,
    )
    argParser.add_argument(
        "--header", help="name of fields", nargs="+", default="", required=False
    )

    argParser.add_argument(
        "--grpattr",
        help="group the sequences based on this attribute",
        type=str,
        default="",
    )

    argParser.add_argument(
        "--attr", help="Attribute to run mining on", type=str, required=True
    )

    argParser.add_argument("--split", help="split the sequences", type=str, default="")
    argParser.add_argument(
        "--merge",
        help="merge the events in the file 1. Dictionary 2. Regex",
        type=int,
        default=0,
    )

    argParser.add_argument(
        "--mergefile", help="merge the events in the file", type=str, default=""
    )

    argParser.add_argument("--output", help="Path of output file", type=str, default="")

    args = argParser.parse_args()
    print(args)

    if not args.output:
        if args.local:
            args.output = (
                os.path.dirname(os.path.abspath(args.file)) + "/output_minsupport/"
            )
            print(f" Output path {args.output}")
            # basename = os.path.splitext(os.path.basename(args.file))[0]
    if not os.path.exists(args.output):
        os.makedirs(args.output)

    # Eventstore creates a list of events
    eventStore = EventStore()
    if args.evttype == 1:
        eventStore.importPointEvents(
            args.file,
            args.startidx,
            args.format,
            sep=args.sep,
            local=args.local,
            header=args.header,
        )
    elif args.evttype == 2:
        eventStore.importIntervalEvents(
            args.file,
            args.startidx,
            args.endidx,
            args.format,
            sep=args.sep,
            local=args.local,
            header=args.header,
        )
    else:
        eventStore.importMixedEvents(
            args.file,
            args.startidx,
            args.endidx,
            args.format,
            sep=args.sep,
            local=args.local,
            header=args.header,
        )

    # create Sequences from Eventstore
    if args.merge:
        if args.merge == 1:
            aggregateEventsDict(eventStore, "dict.txt", args.attr)
        elif args.merge == 2:
            aggregateEventsRegex(eventStore, "dict.txt", args.attr)

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

    # rawSeq = "\n".join(seqs.getEventsString(args.attr) for seqs in seqList)

    print(eventStore.reverseAttrDict[args.attr])

    minSupParam = 0.05
    while minSupParam <= 0.30:
        # stm = SentenTreeMiner(minSup=0.2*len(seqList), maxSup=len(seqList))
        stm = SentenTreeMiner(
            args.attr, minSup=minSupParam * len(seqList), maxSup=len(seqList)
        )
        graph = stm.runSentenTreeMiner(seqList)
        # cfm.truncateSequences(self, seqs, hashVal, evtAttr, node,trailingSeqSegs, notContain)

        # x = json.dumps(root, ensure_ascii=False,
        #                default=RawNode.jsonSerializeDump, indent=1)
        # print("\n\n*****SentenTree output GraphNode******\n\n")

        # x = json.dumps(root, ensure_ascii=False,
        #                default=GraphNode.jsonSerializeDump, indent=1)
        # print(x)

        print("\n\n*****SentenTree Graph output******\n\n")

        y = json.dumps(
            graph, ensure_ascii=False, default=Graph.jsonSerializeDump, indent=1
        )
        print(y)
        with open(
            args.output + "+sententree_msp" + f"{minSupParam:.2f}" + ".json", "w"
        ) as the_file2:
            the_file2.write(y)
        minSupParam += 0.05

        # with open(args.output+'outfile.json', 'w') as the_file:
        #     the_file.write(x)
