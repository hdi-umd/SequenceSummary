# utils/data_loader.py
import os
import json
from datamodel.EventStore import EventStore
from datamodel.Sequence import Sequence
from datamodel.EventAggregate import aggregateEventsDict, aggregateEventsRegex


def load_event_store(args):
    """
    Load data into an EventStore based on event type and other arguments.

    Args:
        args: Command line arguments parsed by argparse

    Returns:
        EventStore: Populated event store object
    """
    print(f"Loading data from {args.file}")
    eventStore = EventStore()

    # Import events based on the specified event type
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

    # Apply merging if requested
    if args.merge:
        if args.merge == 1:
            aggregateEventsDict(eventStore, "dict.txt", args.attr)
        elif args.merge == 2:
            aggregateEventsRegex(eventStore, "dict.txt", args.attr)

    return eventStore


def generate_sequences(eventStore, args):
    """
    Generate sequences from EventStore based on arguments.

    Args:
        eventStore: Populated EventStore object
        args: Command line arguments parsed by argparse

    Returns:
        list: List of Sequence objects
    """
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

    print(f"Generated {len(seqList)} sequences")
    return seqList


def ensure_output_directory(args):
    """
    Ensure the output directory exists.

    Args:
        args: Command line arguments parsed by argparse

    Returns:
        str: Path to output directory
    """
    if not args.output:
        if args.local:
            args.output = os.path.dirname(os.path.abspath(args.file)) + "/output/"
            print(f"Output path: {args.output}")

    if not os.path.exists(args.output):
        os.makedirs(args.output)
        print(f"Created output directory: {args.output}")

    return args.output


def save_json_output(data, filename, json_serializer=None):
    """Save data as JSON with consistent formatting"""
    with open(filename, "w") as file:
        json.dump(data, file, ensure_ascii=False, indent=2, default=json_serializer)
    print(f"Output saved to {filename}")
