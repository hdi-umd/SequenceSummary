"""Implements the main method that calls and executes
SequenceSynopsis module.
"""

import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# from SequenceSynopsisMiner import SequenceSynopsisMiner
# from SequenceSynopsisMinerWithLSH import SequenceSynopsisMiner

import os
import json
import argparse
import csv
from sequence_summary.datamodel.event_store import EventStore
from sequence_summary.datamodel.sequence import Sequence
from sequence_summary.core.graph import Graph

# from sequence_summary.mining.sequencesynopsis.sequence_synopsis_miner_with_weighted_lsh import (
#     SequenceSynopsisMiner,
# )
from sequence_summary.utils.args_parser import (
    get_common_parser,
    add_sequencesynopsis_args,
)
from sequence_summary.utils.data_loader import (
    load_event_store,
    generate_sequences,
    ensure_output_directory,
)


def print_attributes(obj, indent=0):
    for attr in dir(obj):
        if not attr.startswith("__"):  # Exclude built-in attributes
            value = getattr(obj, attr)
            print("  " * indent + f"{attr}: {value}")
            if not isinstance(value, (int, float, str, bool, type(None))):
                print_attributes(value, indent + 1)


def process_results(result, args, event_store):
    """Process and save SequenceSynopsis results."""
    ssm = result[0]  # Clusters
    grph = result[1]  # Graph

    # Export graph to JSON
    z = json.dumps(
        grph, ensure_ascii=False, default=Graph.json_serialize_dump, indent=1
    )
    with open("+seqsynopsis_msp.json", "w") as file:
        file.write(z)

    # Create output directory if needed
    outdir = "output"
    if not os.path.exists(outdir):
        os.mkdir(outdir)

    # Write results to CSV
    pattern2seq = {}
    with open(
        os.path.join(
            outdir,
            f"sequence_synopsis_outfile_{args.fileIdentifier}_alpha{args.alpha}_lambda{args.lambdaVal}.csv",
        ),
        "w",
    ) as the_file:
        writer = csv.writer(the_file)
        writer.writerow(["Pattern_ID", "Event", "Average_Index", "Number of Sequences"])

        for index, elem in enumerate(ssm):
            writer.writerow(["P" + str(index), "_Start", 0, str(len(elem.seq_list))])
            ids = [item._id for item in elem.seq_list]

            if index in pattern2seq:
                pattern2seq[index].extend(ids)
            else:
                pattern2seq[index] = ids

            key_events = event_store.get_event_value(args.attr, elem.pattern.key_evts)

            for ind, pos in enumerate(key_events):
                writer.writerow(
                    ["P" + str(index), pos, elem.index[ind], str(len(elem.seq_list))]
                )

            trailing_len = sum(len(x.events) for x in elem.seq_list) / len(
                elem.seq_list
            )
            writer.writerow(
                ["P" + str(index), "_Exit", trailing_len, str(len(elem.seq_list))]
            )

    # Write pattern to sequence mapping as JSON
    with open(
        os.path.join(
            outdir,
            f"sequence_synopsis_pattern2sequence_{args.fileIdentifier}_alpha{args.alpha}_lambda{args.lambdaVal}.json",
        ),
        "w",
    ) as out_f:
        json.dump(pattern2seq, out_f)

    # Write clusters as JSON
    x = json.dumps(
        [elem.json_default_dump(args.attr, event_store) for elem in ssm],
        ensure_ascii=False,
    )
    with open(
        os.path.join(
            outdir,
            f"sequence_synopsis_outfile_{args.fileIdentifier}_alpha{args.alpha}_lambda{args.lambdaVal}.json",
        ),
        "w",
    ) as the_file:
        the_file.write(x)


def run_with_lsh():
    """Entry point for LSH-based SequenceSynopsis implementation."""
    # Code using SequenceSynopsisMinerWithLSH
    from sequence_summary.mining.sequencesynopsis.sequence_synopsis_miner_with_lsh import (
        SequenceSynopsisMiner,
    )

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
    process_results(result, args, eventStore)


def run_with_weighted_lsh():
    """Entry point for weighted LSH-based SequenceSynopsis implementation."""
    # Code using SequenceSynopsisMinerWithWeightedLSH
    from sequence_summary.mining.sequencesynopsis.sequence_synopsis_miner_with_weighted_lsh import (
        SequenceSynopsisMiner,
    )

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
    process_results(result, args, eventStore)


def run_basic():
    # Get the parser with common arguments and add Sequence Synopsis-specific arguments
    from sequence_summary.mining.sequencesynopsis.sequence_synopsis_miner import (
        SequenceSynopsisMiner,
    )

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
    # Process and save results
    process_results(result, args, eventStore)


def main():
    """Main entry point for SequenceSynopsis. Uses the weighted LSH implementation by default."""
    run_with_weighted_lsh()


if __name__ == "__main__":
    main()
