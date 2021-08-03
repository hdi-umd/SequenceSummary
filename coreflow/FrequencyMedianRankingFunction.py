"""Implements FrequencyMedianRankingFunction."""

from Pattern import Pattern


class FrequencyMedianRankingFunction:
    """Select the event which is present is highest number of sequences
    with smallest medianPos.
    """

    def __init__(self):
        self.topRankedEvtValues = []
        self.evtAttr = ""

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

        self.topRankedEvtValues = sorted(
            self.topRankedEvtValues, key=lambda x: x.getEventMedianPos()[0])

        return self.topRankedEvtValues[0]

    def performRanking(self, seqs, maxSup, excludedEvts):
        """Rank the events based on support (can be number of sequences present in/
        number of occurrences)"""
        result = {}
        uniqueHashes = []
        evtValueKey = ""

        for seq in seqs:
            # get hashlist for each individual sequence
            uniqueHashes = seq.getUniqueValueHashes(self.evtAttr)
            for hashVal in uniqueHashes:
                if hashVal in excludedEvts:
                    continue
                evtValueKey = str(hashVal)

                # create a pattern for all hash values
                if evtValueKey not in result.keys():
                    pat = Pattern([evtValueKey])
                    result[evtValueKey] = pat

                result[evtValueKey].addToSupportSet(seq)
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
