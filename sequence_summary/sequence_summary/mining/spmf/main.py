"""Runs the SPMF algorithm."""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import argparse
import pandas as pd
from spmf import Spmf
from sequence_summary.datamodel.event_store import EventStore
from sequence_summary.datamodel.sequence import Sequence
from sequence_summary.utils.args_parser import get_common_parser, add_spmf_args
from sequence_summary.utils.data_loader import (
    load_event_store,
    generate_sequences,
    ensure_output_directory,
)


def runSPMF(sequence, attr, argsSPMF, output=None):
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
    if output:
        dataFrame.to_csv(output, index=False)


def main():
    # Get the parser with common arguments and add SPMF-specific arguments
    parser = get_common_parser()
    parser = add_spmf_args(parser)
    args = parser.parse_args()
    print(args)

    # Ensure output directory exists
    output_path = ensure_output_directory(args)

    # Load data
    eventStore = load_event_store(args)

    # Generate sequences
    seqList = generate_sequences(eventStore, args)

    # Run SPMF
    print("\n*****Running SPMF*****\n")
    output_file = f"{output_path}_spmf_results.csv" if args.output else None
    runSPMF(seqList, args.attr, [1], output_file)
    print("\n*****SPMF processing completed*****\n")


if __name__ == "__main__":
    main()
