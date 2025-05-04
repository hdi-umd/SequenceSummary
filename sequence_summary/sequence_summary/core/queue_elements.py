"""Implements QueueElements class for the Priority Queuein Sequence Synopsis."""

class QueueElements:
    """Holds the infromation of clusters to merge, description length
    reduction and the optimal cluster value.
    """

    def __init__(self, reduction, optimalC, clus1, clus2):

        self.deltaL = reduction
        self.cStar = optimalC
        self.clust1 = clus1
        self.clust2 = clus2

    def printElement(self, attr):
        """Print Queueelements"""
        print(f'deltaL {self.deltaL}')
        print(f'cStar {self.cStar.printClust(attr)}')
        print(f'clust1 {self.clust1.printClust(attr)}')
        print(f'clust2 {self.clust2.printClust(attr)}')

    @staticmethod
    def printPriorityQueue(priorQ, attr):
        """Prints a priority queue list."""
        print("---PriorityQueue---")
        for elem in priorQ:
            elem.printElement(attr)
        print("------------------------------")
