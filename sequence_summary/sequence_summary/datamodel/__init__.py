"""
Data model components for event sequences.

This module provides classes for working with event sequence data:

- Event: Base class for events (point and interval)
- EventStore: Container for handling collections of events
- Sequence: Ordered collection of events sharing a common property
- EventAggregate: Utilities for aggregating similar events
"""

from .event import Event, PointEvent, IntervalEvent
from .event_store import EventStore
from .sequence import Sequence
from .event_aggregate import aggregateEventsRegex, aggregateEventsDict
