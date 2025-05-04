"""Runs the SPMF algorithm."""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import argparse
import pandas as pd
from spmf import Spmf
from datamodel.EventStore import EventStore
from datamodel.Sequence import Sequence
from utils.args_parser import get_common_parser, add_spmf_args


def runSPMF(sequence, attr, argsSPMF):
    """This module runs spmf using the py-spmf package."""

    # convert input to list format
    if not isinstance(sequence, list):
        sequence = [sequence]
    rawSeq = ""
    for seqs in sequence:
        # cdist is the same for all sequences
        cstr, cdist = seqs.convertToVMSPReadable(attr)
        rawSeq += cstr + "\n"

    spmf = Spmf(
        "VMSP",
        spmf_bin_location_dir="./",
        input_direct=rawSeq,
        input_type="text",
        output_filename="output.txt",
        arguments=argsSPMF,
    )

    spmf.run()
    # get num2character mapping:
    num2char = {}
    for key, val in cdist.items():
        num2char[val] = key
    dataFrame = spmf.to_pandas_dataframe(pickle=True)
    dataFrame["patternLetter"] = dataFrame["pattern"].apply(
        lambda x: [num2char[i] for i in x]
    )

    # more options can be specified also
    with pd.option_context("display.max_rows", 10, "display.max_columns", None):
        print(dataFrame)
    if args.output:
        dataFrame.to_csv(args.output, index=False)


def main():
    # Get the parser with common arguments and add SPMF-specific arguments
    parser = get_common_parser()
    parser = add_spmf_args(parser)
    args = parser.parse_args()
    print(args)

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

    print("\n\n*****SPMF output******\n\n")
    runSPMF(seqList, args.attr, [1])
    print("\n\n")


if __name__ == "__main__":
    main()
