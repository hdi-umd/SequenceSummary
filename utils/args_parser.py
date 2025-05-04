# utils/args_parser.py

import argparse


def get_common_parser():
    """Create a parser with arguments common to all techniques"""
    parser = argparse.ArgumentParser()

    # Input file arguments
    parser.add_argument(
        "--file",
        help="File to read from",
        type=str,
        default="../Sample_Dataset.csv",
        required=False,
    )
    parser.add_argument(
        "--evttype",
        help="1. Point 2.Interval 3.Mixed event",
        type=int,
        default=1,
        required=False,
    )
    parser.add_argument(
        "--startidx",
        help="Column Index of starting time",
        type=int,
        default=0,
        required=False,
    )
    parser.add_argument(
        "--endidx",
        help="Column Index of ending time",
        type=int,
        default=1,
        required=False,
    )
    parser.add_argument(
        "--format", help="Time format", type=str, default="%m/%d/%y", required=False
    )
    parser.add_argument(
        "--sep", help="separator of fields", type=str, default=",", required=False
    )
    parser.add_argument(
        "--local",
        help="Local availability of file",
        type=bool,
        default=True,
        required=False,
    )
    parser.add_argument(
        "--header", help="name of fields", nargs="+", default="", required=False
    )

    # Event sequence arguments
    parser.add_argument(
        "--attr", help="Attribute to run mining on", type=str, required=True
    )
    parser.add_argument(
        "--grpattr",
        help="group the sequences based on this attribute",
        type=str,
        default="",
    )
    parser.add_argument("--split", help="split the sequences", type=str, default="")

    # Output arguments
    parser.add_argument("--output", help="Path of output file", type=str, default="./")

    # Event merging arguments
    parser.add_argument(
        "--merge",
        help="merge the events in the file 1. Dictionary 2. Regex",
        type=int,
        default=0,
    )
    parser.add_argument(
        "--mergefile", help="merge the events in the file", type=str, default=""
    )

    return parser


def add_coreflow_args(parser):
    """Add CoreFlow-specific arguments"""
    parser.add_argument(
        "--minsup",
        help="Minimum support threshold (0.0-1.0)",
        type=float,
        default=0.2,
        required=False,
    )
    return parser


def add_sententree_args(parser):
    """Add SentenTree-specific arguments"""
    parser.add_argument(
        "--minsup",
        help="Minimum support threshold (0.0-1.0)",
        type=float,
        default=0.2,
        required=False,
    )
    return parser


def add_sequencesynopsis_args(parser):
    """Add Sequence Synopsis-specific arguments"""
    parser.add_argument(
        "--alpha",
        help="Balance between info loss and visual complexity",
        type=float,
        default=0.99,
    )
    parser.add_argument(
        "--lambdaVal",
        help="Balance between pattern count and edit operations",
        type=float,
        default=0.01,
    )
    parser.add_argument("--fileIdentifier", type=str, default="")
    return parser


def add_spmf_args(parser):
    """Add SPMF-specific arguments"""
    # Add any SPMF-specific arguments here
    return parser
