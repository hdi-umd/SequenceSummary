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
from datetime import timedelta
from memory_profiler import memory_usage
from utils.args_parser import (
    get_common_parser,
    add_coreflow_args,
    add_sententree_args,
    add_sequencesynopsis_args,
)
from utils.data_loader import (
    load_event_store,
    generate_sequences,
    ensure_output_directory,
)

from core.Node import TreeNode, GraphNode
from datamodel.Sequence import Sequence
from core.Graph import Graph
from datamodel.EventStore import EventStore
from datamodel.EventAggregate import aggregateEventsRegex, aggregateEventsDict
from coreflow.CoreFlowMiner import CoreFlowMiner
from sententree.SentenTreeMiner import SentenTreeMiner
from sequencesynopsis.SequenceSynopsisMinerWithWeightedLSH import SequenceSynopsisMiner
from sequencesynopsis.SequenceSynopsisMiner import SequenceSynopsisMiner as ssmv


def main():
    parser = get_common_parser()
    # Add all technique-specific arguments
    parser = add_coreflow_args(parser)
    # parser = add_sententree_args(parser)
    parser = add_sequencesynopsis_args(parser)
    args = parser.parse_args()
    print(args)

    # Ensure output directory exists
    output_path = ensure_output_directory(args)

    # Get basename for output files
    basename = os.path.splitext(os.path.basename(args.file))[0]

    # Load data - this only needs to be done once for all techniques
    eventStore = load_event_store(args)
    seqList = generate_sequences(eventStore, args)

    Sequence.seqListtotsv(seqList, args.attr)

    with open(
        "TimeMemoryAnalysis.csv", "a"
    ) as timeFile:  # , open('MemAnalysis.csv', 'w') as memFile:
        writer = csv.writer(timeFile)
        writer.writerow(["Dataset", "Support", "Tool", "Time", "Memory"])
        # memWriter = csv.writer(memFile)
        # writer.writerow(["Dataset", "Support", "Tool", "Memory"])

        minSupParam = 0.05
        while minSupParam <= 0.3:
            cfm = CoreFlowMiner(
                args.attr, minSup=minSupParam * len(seqList), maxSup=len(seqList)
            )

            start = time.time()
            mem, output = memory_usage(
                proc=[cfm.runCoreFlowMiner, [seqList]],
                include_children=True,
                max_usage=True,
                retval=True,
            )
            end = time.time()
            root = output[0]
            graph = output[1]

            writer.writerow(
                [
                    basename,
                    f"{minSupParam:.2f}",
                    "Coreflow",
                    timedelta(seconds=end - start),
                    mem,
                ]
            )

            print("\n\n*****Coreflow output******\n\n")

            x = json.dumps(
                root, ensure_ascii=False, default=TreeNode.jsonSerializeDump, indent=1
            )
            print(x)

            with open(
                output_path
                + basename
                + "+coreflow_msp"
                + f"{minSupParam:.2f}"
                + ".json",
                "w",
            ) as the_file:
                the_file.write(x)

            stm = SentenTreeMiner(
                args.attr, minSup=minSupParam * len(seqList), maxSup=len(seqList)
            )
            start = time.time()
            mem, graph = memory_usage(
                proc=[stm.runSentenTreeMiner, [seqList]],
                include_children=True,
                max_usage=True,
                retval=True,
            )
            end = time.time()

            writer.writerow(
                [
                    basename,
                    f"{minSupParam:.2f}",
                    "Sententree",
                    timedelta(seconds=end - start),
                    mem,
                ]
            )

            print("\n\n*****SentenTree Graph output******\n\n")

            y = json.dumps(
                graph, ensure_ascii=False, default=Graph.jsonSerializeDump, indent=1
            )
            print(y)
            # with open(args.output+'sententree_result.json', 'w') as the_file1:
            #     the_file1.write(x)

            with open(
                output_path
                + basename
                + "+sententree_msp"
                + f"{minSupParam:.2f}"
                + ".json",
                "w",
            ) as the_file2:
                the_file2.write(y)

            ssm = SequenceSynopsisMiner(
                args.attr, eventStore, alpha=minSupParam, lambdaVal=1 - minSupParam
            )
            start = time.time()
            mem, output = memory_usage(
                proc=[ssm.minDL, [seqList]],
                include_children=True,
                max_usage=True,
                retval=True,
            )
            end = time.time()
            writer.writerow(
                [
                    basename,
                    f"{minSupParam:.2f}",
                    "SyquenceSynopsis",
                    timedelta(seconds=end - start),
                    mem,
                ]
            )
            clust = output[0]
            grph = output[1]
            print(clust)
            z = json.dumps(
                grph, ensure_ascii=False, default=Graph.jsonSerializeDump, indent=1
            )
            print(z)

            # with open(args.output+'sententree_result.json', 'w') as the_file1:
            #     the_file1.write(x)

            with open(
                output_path
                + basename
                + "+seqsynopsis_alpha"
                + f"{minSupParam:.2f}"
                + ".json",
                "w",
            ) as the_file3:
                the_file3.write(z)
            ssmvanilla = ssmv(
                args.attr, eventStore, alpha=minSupParam, lambdaVal=1 - minSupParam
            )
            start = time.time()
            mem, output = memory_usage(
                proc=[ssmvanilla.minDL, [seqList]],
                include_children=True,
                max_usage=True,
                retval=True,
            )
            end = time.time()
            writer.writerow(
                [
                    basename,
                    f"{minSupParam:.2f}",
                    "SyquenceSynopsisvanilla",
                    timedelta(seconds=end - start),
                    mem,
                ]
            )

            minSupParam += 0.05
            clust = output[0]
            grph = output[1]

            z = json.dumps(
                grph, ensure_ascii=False, default=Graph.jsonSerializeDump, indent=1
            )
            print(z)


if __name__ == "__main__":
    main()
