"""Implements cluster class."""

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

    def jsonDefaultDump(self, attr, evtStore) -> dict:
        """Jsonify a cluster onject"""
        return {
            "pattern": evtStore.getEventValue(attr, self.pattern.keyEvts),
            "sequences": [val.getEvtAttrValues(attr) for val in self.seqList]
        }

    @staticmethod
    def printClustDict(clustD, attr):
        """Prints an array of clusters"""
        print("------key val pairs----")
        for entries in clustD:
            entries.printClust(attr)
