"""Implements all RankingFunction."""

from collections import Counter
from Pattern import Pattern


class RankingFunction:
    """ Class to perform ranking and tiebreaker among events. """

    def __init__(self, attr, maxSup):
        self.topRankedEvtValues = []
        self.evtAttr = attr
        self.maxSupport = maxSup
        self.rankingFunc = self.numberOfSequence
        self.tieBreaker = self.performRankingMedianIndex  # self.

    def setRankingFunc(self, method1):
        """Set ranking function."""
        self.rankingFunc = method1

    def setTieBreaker(self, method1):
        """Set tie breaker."""
        self.tieBreaker = method1

    def setEvtAttr(self, evtAttr):
        """Assigns the evtAttr value for Ranking Function."""
        self.evtAttr = evtAttr

    def getTopEventSet(self):
        """returns the top ranked event where tiebreaker is calculated based
        on specific Ranking function.
        """
        if not self.topRankedEvtValues:
            return None
        if len(self.topRankedEvtValues) == 1:
            return self.topRankedEvtValues[0]

        for pat in self.topRankedEvtValues:
            pat.computePatternStats(self.evtAttr)

        self.topRankedEvtValues = self.tieBreaker()

        print(f'top ranked{self.topRankedEvtValues[0].keyEvts}')

        return self.topRankedEvtValues[0]

    def performRanking(self, seqs):
        """Rank the events based on support (can be number of sequences present in/
        number of occurrences)"""
        result = Counter()
        patternDict = {}

        for seq in seqs:
            # get hashlist for each individual sequence
            eventHashes = self.rankingFunc(seq)
            for hashVal in eventHashes:
                result[hashVal] += 1
                if hashVal not in patternDict.keys():
                    patternDict[hashVal] = Pattern(hashVal)
                patternDict[hashVal].addToSupportSet(seq.sid)

        #print(f'result {result}')

        # Get most common tuples
        self.topRankedEvtValues = []
        candidate = []
        maxVal = 0
        if result:
            for val in result.most_common():
                #print(f' common {val}')
                if val[1] > self.maxSupport:
                    continue
                maxVal = val[1]  # find highest elem value
                break
            candidate = [
                val[0] for val in result.most_common() if val[1] == maxVal]
            self.topRankedEvtValues = [elem for elem in patternDict.values()
                                       for cand in candidate if elem.keyEvts == cand]
            print(f'top values {self.topRankedEvtValues}')

    def numberOfSequence(self, sequence):
        """Select the event which is present in highest number of sequences."""
        return sequence.getUniqueValueHashes(self.evtAttr)

    def allOccurrence(self, sequence):
        """Select the event which is present maximum number of time across all sequences."""
        return sequence.getHashList(self.evtAttr)

    def performRankingMedianIndex(self):
        """Select the event which is present is highest number of sequences
        with smallest medianPos.
        """
        return sorted(
            self.topRankedEvtValues, key=lambda x: x.getEventMedianPos()[0])

    def performRankingMeanIndex(self):
        """ Select the event which is present in highest number of sequences
        with smallest meanPos.
        """
        return sorted(
            self.topRankedEvtValues, key=lambda x: x.getEventMeanPos()[0])
