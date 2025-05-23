"""Implements the main method that calls and executes
SequenceSynopsis module.
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import argparse
import csv
from datamodel.EventStore import EventStore
from datamodel.Sequence import Sequence
from core.Graph import Graph
from utils.args_parser import get_common_parser, add_sequencesynopsis_args
from utils.data_loader import (
    load_event_store,
    generate_sequences,
    ensure_output_directory,
)


# from SequenceSynopsisMiner import SequenceSynopsisMiner
# from SequenceSynopsisMinerWithLSH import SequenceSynopsisMiner
from sequencesynopsis.SequenceSynopsisMinerWithWeightedLSH import SequenceSynopsisMiner


def print_attributes(obj, indent=0):
    for attr in dir(obj):
        if not attr.startswith("__"):  # Exclude built-in attributes
            value = getattr(obj, attr)
            print("  " * indent + f"{attr}: {value}")
            if not isinstance(value, (int, float, str, bool, type(None))):
                print_attributes(value, indent + 1)


def main():
    # Get the parser with common arguments and add Sequence Synopsis-specific arguments
    parser = get_common_parser()
    parser = add_sequencesynopsis_args(parser)
    args = parser.parse_args()
    print(args)

    # Ensure output directory exists
    output_path = ensure_output_directory(args)

    # Load data
    eventStore = load_event_store(args)

    # Generate sequences
    seqList = generate_sequences(eventStore, args)

    print(f"\nEvent dictionary: {eventStore.reverseAttrDict[args.attr]}\n")
    print("\nRunning Sequence Synopsis mining...")
    syn = SequenceSynopsisMiner(
        args.attr, eventStore, alpha=args.alpha, lambdaVal=args.lambdaVal
    )
    result = syn.minDL(seqList)
    ssm = result[0]
    grph = result[1]
    z = json.dumps(grph, ensure_ascii=False, default=Graph.jsonSerializeDump, indent=1)
    print("\n\n*****SeqSynopsis output******\n\n")
    print(z)
    with open(output_path + "+seqsynopsis_msp" + ".json", "w") as the_file3:
        the_file3.write(z)
    # print(ssm)
    pattern2seq = {}
    with open(
        os.path.join(
            output_path,
            f"sequence_synopsis_outfile_{args.fileIdentifier}_alpha{args.alpha}_lambda{args.lambdaVal}.csv",
        ),
        "w",
    ) as the_file:
        writer = csv.writer(the_file)
        writer.writerow(["Pattern_ID", "Event", "Average_Index", "Number of Sequences"])
        for index, elem in enumerate(ssm):
            # print(f'elemvalue {elem.index}')
            writer.writerow(["P" + str(index), "_Start", 0, str(len(elem.seqList))])
            ids = [item._id for item in elem.seqList]
            if index in pattern2seq:
                pattern2seq[index].extend(ids)
            else:
                pattern2seq[index] = ids
            # print(ids)
            # print_attributes(elem.seqList[0])
            keyEvents = eventStore.getEventValue(args.attr, elem.pattern.keyEvts)
            # print(f'key {keyEvents}')
            for ind, pos in enumerate(keyEvents):
                # print(f'pos {pos} ind {ind}')
                writer.writerow(
                    ["P" + str(index), pos, elem.index[ind], str(len(elem.seqList))]
                )
            trailingLen = sum(len(x.events) for x in elem.seqList) / len(elem.seqList)
            writer.writerow(
                ["P" + str(index), "_Exit", trailingLen, str(len(elem.seqList))]
            )

    with open(
        os.path.join(
            output_path,
            f"sequence_synopsis_pattern2sequence_{args.fileIdentifier}_alpha{args.alpha}_lambda{args.lambdaVal}.json",
        ),
        "w",
    ) as out_f:
        json.dump(pattern2seq, out_f)

    # Cluster.printClustDict(G, "Event")

    x = json.dumps(
        [elem.jsonDefaultDump(args.attr, eventStore) for elem in ssm],
        ensure_ascii=False,
    )
    # print(x)

    with open(
        os.path.join(
            output_path,
            f"sequence_synopsis_outfile_{args.fileIdentifier}_alpha{args.alpha}_lambda{args.lambdaVal}.json",
        ),
        "w",
    ) as the_file:
        the_file.write(x)

    print("\n*****Sequence Synopsis mining completed*****\n")


if __name__ == "__main__":
    main()
