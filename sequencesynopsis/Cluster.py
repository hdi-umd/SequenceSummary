"""Implements cluster class."""

from Pattern import Pattern
from Sequence import Sequence


class Cluster:
    """Holds the information of a Pattern <List of Sequence> cluster."""

    def __init__(self, pat, seq):
        self.pattern = pat
        self.seqList = seq

    def printClust(self, attr):
        """Prints a cluster"""
        print(f'Pattern {self.pattern.keyEvts}')
        for val in self.seqList:
            print(f'Sequences {val.getHashList(attr)}')

    @staticmethod
    def printClustDict(clustD, attr):
        """Prints an array of clusters"""
        print("------key val pairs----")
        for entries in clustD:
            entries.printClust(attr)
        #    print(f'Pattern {entries.pattern.keyEvts}')
        #    for val in entries.seqList:
        #        print(f'Sequences {val.getHashList(attr)}')
        # for key, value in clustD.items():
        #    print(f'Pattern {key.keyEvts}')
        #    for val in value:
        #        print(f'Sequences {val.getHashList(attr)}')
