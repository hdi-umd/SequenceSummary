"""Implements the main method that calls and executes
Coreflow module.
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.args_parser import get_common_parser, add_coreflow_args
from utils.data_loader import (
    load_event_store,
    generate_sequences,
    ensure_output_directory,
)
from utils.logger import setup_logger
from datamodel.EventStore import EventStore
from datamodel.Sequence import Sequence
from datamodel.EventAggregate import aggregateEventsRegex, aggregateEventsDict
from core.Node import TreeNode
from core.Graph import Graph
from coreflow.CoreFlowMiner import CoreFlowMiner
import argparse
import json

# Set up logger for this module
logger = setup_logger(__name__, "CoreFlow")


def main():
    # Get the parser with common arguments and add CoreFlow-specific arguments
    parser = get_common_parser()
    parser = add_coreflow_args(parser)
    args = parser.parse_args()
    logger.info(f"Arguments: {args}")

    # Ensure output directory exists
    output_path = ensure_output_directory(args)
    logger.info(f"Output directory: {output_path}")

    # Load data
    logger.info(f"Loading data from {args.file}")
    eventStore = load_event_store(args)

    # Generate sequences
    logger.info("Generating sequences")
    seqList = generate_sequences(eventStore, args)
    logger.info(f"Generated {len(seqList)} sequences")

    print(f"\nEvent dictionary: {eventStore.reverseAttrDict[args.attr]}\n")

    print("\nRunning CoreFlow mining...")
    cfm = CoreFlowMiner(
        args.attr, minSup=args.minsup * len(seqList), maxSup=len(seqList)
    )

    # cfm.run(seqList, args.attr, root, 5 * Sequence.getSeqVolume(
    #       seqList)/100.0, Sequence.getSeqVolume(seqList), [], {}, -1)
    root, graph = cfm.runCoreFlowMiner(seqList)

    print("\n\n*****Coreflow output******\n\n")

    x = json.dumps(
        root, ensure_ascii=False, default=TreeNode.jsonSerializeDump, indent=1
    )
    print(x)

    with open(output_path + "coreflow_result.json", "w") as the_file:
        the_file.write(x)

    y = json.dumps(graph, ensure_ascii=False, default=Graph.jsonSerializeDump, indent=1)
    print(y)

    with open(output_path + "coreflow_graph.json", "w") as the_file2:
        the_file2.write(y)
    print("\n*****CoreFlow mining completed*****\n")


if __name__ == "__main__":
    main()
