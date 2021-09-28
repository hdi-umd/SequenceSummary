"""Implements cluster class."""
# import csv
class Cluster:
    """Holds the information of a Pattern <List of Sequence> cluster."""

    def __init__(self, pat, seq, ind=None):
        if ind is None:
            ind = []
        self.pattern = pat
        self.seqList = seq
        self.index = ind

    def printClust(self, attr):
        """Prints a cluster"""
        print(f'Pattern {self.pattern.keyEvts}')
        print(f'positions {self.index}')
        for val in self.seqList:
            print(f'Sequences {val.getHashList(attr)}')

    # def writeToCSV(self, filename):
    #     with open(filename, 'w') as the_file:
    #         writer = csv.writer(the_file)
    #         writer.writerow(["Pattern_ID, Event, Average_Index"])
    #         for elem in self.


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
