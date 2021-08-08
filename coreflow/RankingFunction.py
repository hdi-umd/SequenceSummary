"""Implements all RankingFunction."""

from Pattern import Pattern


class RankingFunction:
    """ Class to perform ranking and tiebreaker among events. """

    def __init__(self):
        self.topRankedEvtValues = []
        self.evtAttr = ""
        self.rankingFunc = self.numberOfSequence
        self.tieBreaker = self.performRankingMedianIndex#self.

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

        print(f'top ranked{self.topRankedEvtValues[0]}')

        return self.topRankedEvtValues[0]

    def performRanking(self, seqs, maxSup, excludedEvts):
        """Rank the events based on support (can be number of sequences present in/
        number of occurrences)"""
        result = {}
        evtValueKey = ""

        for seq in seqs:
            # get hashlist for each individual sequence
            eventHashes = self.rankingFunc(seq)
            for hashVal in eventHashes:
                if hashVal in excludedEvts:
                    continue
                evtValueKey = str(hashVal)

                # create a pattern for all hash values
                if evtValueKey not in result.keys():
                    pat = Pattern([evtValueKey])
                    result[evtValueKey] = pat

                result[evtValueKey].addToSupportSet(seq.sid)
        candidates = []

        for itr in result.values():
            if itr.getSupport() > maxSup:
                continue
            candidates.append(itr)

        if not candidates:
            return

        candidates = sorted(
            candidates, key=lambda x: x.getSupport(), reverse=True)

        self.topRankedEvtValues = []

        maxval = candidates[0].getSupport()

        for patterns in candidates:
            if patterns.getSupport() < maxval:
                break
            self.topRankedEvtValues.append(patterns)


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
