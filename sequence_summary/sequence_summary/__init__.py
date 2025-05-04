"""
Sequence Summary: A library for visual summarization of event sequences.

This package provides implementations of various event sequence visualization techniques:
- CoreFlow: Tree-structured visualizations highlighting branching patterns
- SentenTree: Graph-based visualizations showing event relationships
- SequenceSynopsis: Optimized visual summaries using minimum description length principle
"""

__version__ = "0.1.0"

# Core components
from .core.cluster import Cluster
from .core.graph import Graph, RawNode, Links
from .core.node import Node, TreeNode, GraphNode
from .core.pattern import Pattern
from .core.queue_elements import QueueElements

# Data model
from .datamodel.event import Event, PointEvent, IntervalEvent
from .datamodel.event_store import EventStore
from .datamodel.sequence import Sequence
from .datamodel.event_aggregate import aggregateEventsRegex, aggregateEventsDict

# Mining techniques
from .mining.coreflow.coreflow_miner import CoreFlowMiner
from .mining.sententree.sententree_miner import SentenTreeMiner
from .mining.sequencesynopsis import SequenceSynopsisMiner

# Utils
from .utils.helper import getDataframe, getTimeToSortBy, insertEventIntoDict
from .utils.args_parser import (
    get_common_parser,
    add_coreflow_args,
    add_sententree_args,
    add_sequencesynopsis_args,
)
from .utils.data_loader import (
    load_event_store,
    generate_sequences,
    ensure_output_directory,
)
from .utils.logger import setup_logger
