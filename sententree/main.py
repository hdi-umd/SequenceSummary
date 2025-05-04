"""Implements the main method that calls and executes SentenTree modules."""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.Graph import Graph
from sententree.SentenTreeMiner import SentenTreeMiner
import json
from utils.args_parser import get_common_parser, add_sententree_args
from utils.data_loader import (
    load_event_store,
    generate_sequences,
    ensure_output_directory,
)


def main():
    # Get the parser with common arguments and add SentenTree-specific arguments
    parser = get_common_parser()
    parser = add_sententree_args(parser)
    args = parser.parse_args()
    print(args)

    # Ensure output directory exists
    output_path = ensure_output_directory(args)

    # Load data
    eventStore = load_event_store(args)

    # Generate sequences
    seqList = generate_sequences(eventStore, args)

    print(f"\nEvent dictionary: {eventStore.reverseAttrDict[args.attr]}\n")

    print("Running SentenTree mining...")
    stm = SentenTreeMiner(
        args.attr, minSup=args.minsup * len(seqList), maxSup=len(seqList)
    )
    graph = stm.runSentenTreeMiner(seqList)
    print("\n\n*****SentenTree Graph output******\n\n")

    y = json.dumps(graph, ensure_ascii=False, default=Graph.jsonSerializeDump, indent=1)
    print(y)
    with open(
        output_path + "+sententree_msp" + f"{args.minsup:.2f}" + ".json", "w"
    ) as the_file2:
        the_file2.write(y)

    # with open(args.output+'outfile.json', 'w') as the_file:
    #     the_file.write(x)
    print("\n*****SentenTree mining completed*****\n")


if __name__ == "__main__":
    main()
