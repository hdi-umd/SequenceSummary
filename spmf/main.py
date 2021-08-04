"""Runs the SPMF algorithm."""


import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import argparse
import pandas as pd
from spmf import Spmf
from EventStore import EventStore
from Sequence import Sequence


def runSPMF(sequence, attr, argsSPMF):
    """This module runs spmf using the py-spmf package."""

    # convert input to list format
    if not isinstance(sequence, list):
        sequence = [sequence]

    rawSeq = "\n".join(seqs.convertToVMSPReadable(attr) for seqs in sequence)

    spmf = Spmf("VMSP", spmf_bin_location_dir="./", input_direct=rawSeq,
                input_type="text", output_filename="output.txt", arguments=argsSPMF)

    spmf.run()
    dataFrame = spmf.to_pandas_dataframe(pickle=True)

    # more options can be specified also
    with pd.option_context('display.max_rows', 10, 'display.max_columns', None):
        print(dataFrame)


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

    print("\n\n*****SPMF output******\n\n")
    runSPMF(seqList, args.attr, [0.5])
    print("\n\n")
