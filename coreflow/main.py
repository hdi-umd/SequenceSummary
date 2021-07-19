import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from EventStore import EventStore
from CoreFlowMiner import CoreFlowMiner
from Sequence import Sequence
from TreeNode import TreeNode
from spmf import Spmf
import pandas as pd
import json
import argparse


def run_spmf(sequence, attr, args_spmf):
    """This module runs spmf using the py-spmf package."""

    # convert input to list format
    if not isinstance(sequence, list):
        sequence = [sequence]

    raw_seq = "\n".join(seqs.convertToVMSPReadable(attr) for seqs in sequence)

    spmf = Spmf("VMSP", spmf_bin_location_dir="./", input_direct=raw_seq,
                input_type="text", output_filename="output.txt", arguments=args_spmf)

    spmf.run()
    df = spmf.to_pandas_dataframe(pickle=True)

    # more options can be specified also
    with pd.option_context('display.max_rows', 10, 'display.max_columns', None):
        print(df)


if __name__ == "__main__":
    # main()

    argparser = argparse.ArgumentParser()
    argparser.add_argument("--file", help="File to read from",
                           type=str, default="sequence_braiding_refined.csv", required=False)
    argparser.add_argument("--evttype", help="1. Point 2.Interval 3.Mixed event",
                           type=int, default=1, required=False)
    argparser.add_argument("--startidx", help="Column Index of starting time",
                           type=int, default=0, required=False)
    argparser.add_argument("--endidx", help="Column Index of ending time",
                           type=int, default=1, required=False)
    argparser.add_argument("--format", help="Time format",
                           type=str, default="%m/%d/%y", required=False)

    argparser.add_argument("--sep", help="separator of fields",
                           type=str, default=",", required=False)
    argparser.add_argument("--local", help="Local availability of file",
                           type=bool, default=True, required=False)
    argparser.add_argument("--spmf", help="Run spmf",
                           type=bool, default=False)

    argparser.add_argument("--attr", help="Attribute to run mining on",
                           type=str, required=True)

    argparser.add_argument("--grpattr", help="group the sequences based on this attribute",
                           type=str, default="")

    argparser.add_argument("--split", help="split the sequences",
                           type=str, default="")

    argparser.add_argument("--output", help="Path of output file",
                           type=str, default="")

    args = argparser.parse_args()
    print(args)

    # Eventstore creates a list of events
    Es = EventStore()
    if(args.evttype == 1):
        Es.importPointEvents(args.file, args.startidx,
                             args.format, sep=args.sep, local=args.local)
    elif(args.evttype == 2):
        Es.importIntervalEvents(
            args.file, args.startidx, args.endidx, args.format, sep=args.sep, local=args.local)
    else:
        Es.importMixedEvents(args.file, args.startidx, args.endidx,
                             args.format, sep=args.sep, local=args.local)

    # create Sequences from Eventstore

    if(args.grpattr):
        seq = Es.generateSequence(args.grpattr)
    else:
        seq = Sequence(Es.events, Es)

    if(args.split):
        seq_list = Sequence.splitSequences(seq, args.split)
    else:
        if not isinstance(seq, list):
            seq_list = [seq]
        else:
            seq_list = seq

    if(args.spmf == True):
        print("\n\n*****SPMF output******\n\n")
        run_spmf(seq_list, args.attr, [0.5])
        print("\n\n")

    cfm = CoreFlowMiner()
    root = cfm.getNewRootNode(Sequence.getSeqVolume(
        seq_list), seq_list, attr=args.attr)
    #cfm.run(seq_list, args.attr, root, 5 * Sequence.getSeqVolume(seq_list)/100.0, Sequence.getSeqVolume(seq_list), [], {}, -1)
    cfm.run(seq_list, args.attr, root, 2,
            Sequence.getSeqVolume(seq_list), [], {}, -1)

    print("\n\n*****Coreflow output******\n\n")

    x = json.dumps(root, ensure_ascii=False,
                   default=TreeNode.json_serialize_dump, indent=1)
    print(x)

    with open(args.output+'outfile.json', 'w') as the_file:
        the_file.write(x)
