"""Implements the main method that calls and executes SentenTree modules."""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from datamodel.EventStore import EventStore
from datamodel.EventAggregate import aggregateEventsRegex, aggregateEventsDict
from datamodel.Sequence import Sequence
from core.Graph import Graph
from sententree.SentenTreeMiner import SentenTreeMiner
import json
from utils.args_parser import get_common_parser, add_sententree_args


def main():
    # Get the parser with common arguments and add SentenTree-specific arguments
    parser = get_common_parser()
    parser = add_sententree_args(parser)
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

    stm = SentenTreeMiner(
        args.attr, minSup=args.minsup * len(seqList), maxSup=len(seqList)
    )
    graph = stm.runSentenTreeMiner(seqList)
    print("\n\n*****SentenTree Graph output******\n\n")

    y = json.dumps(graph, ensure_ascii=False, default=Graph.jsonSerializeDump, indent=1)
    print(y)
    with open(
        args.output + "+sententree_msp" + f"{args.minsup:.2f}" + ".json", "w"
    ) as the_file2:
        the_file2.write(y)

    # with open(args.output+'outfile.json', 'w') as the_file:
    #     the_file.write(x)


if __name__ == "__main__":
    main()
