"""Implements the main method that calls and executes
Coreflow module.
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.args_parser import get_common_parser, add_coreflow_args
from datamodel.EventStore import EventStore
from datamodel.Sequence import Sequence
from datamodel.EventAggregate import aggregateEventsRegex, aggregateEventsDict
from core.Node import TreeNode
from core.Graph import Graph
from coreflow.CoreFlowMiner import CoreFlowMiner
import argparse
import json


def main():

    parser = get_common_parser()
    parser = add_coreflow_args(parser)
    args = parser.parse_args()
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

    cfm = CoreFlowMiner(
        args.attr, minSup=args.minsup * len(seqList), maxSup=len(seqList)
    )

    # cfm.run(seqList, args.attr, root, 5 * Sequence.getSeqVolume(
    #       seqList)/100.0, Sequence.getSeqVolume(seqList), [], {}, -1)
    root, graph = cfm.runCoreFlowMiner(seqList)

    print("\n\n*****Coreflow output******\n\n")

    if not os.path.isdir(args.output):
        os.mkdir(args.output)

    x = json.dumps(
        root, ensure_ascii=False, default=TreeNode.jsonSerializeDump, indent=1
    )
    print(x)

    with open(args.output + "coreflow_result.json", "w") as the_file:
        the_file.write(x)

    y = json.dumps(graph, ensure_ascii=False, default=Graph.jsonSerializeDump, indent=1)
    print(y)

    with open(args.output + "coreflow_graph.json", "w") as the_file2:
        the_file2.write(y)


if __name__ == "__main__":
    main()
