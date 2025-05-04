"""Implements ranking methods for coreflow."""

import numpy as np


class RankingFunction:
    """Class to perform ranking and tiebreaker among events."""

    def __init__(self, maxSup):
        self.fdist = {}
        self.fdistInd = {}
        self.pos = -1
        self.word = ""
        self.count = 0
        self.maxSupport = maxSup
        self.rankingFunc = self.numberOfSequence
        self.tieBreaker = self.performRankingMedianIndex  # self.

    def setRankingFunc(self, method1):
        """Set ranking function."""
        self.rankingFunc = method1

    def setTieBreaker(self, method1):
        """Set tie breaker."""
        self.tieBreaker = method1

    def clearfdists(self):
        """clear fdist and fdistInd."""
        self.fdist.clear()
        self.fdistInd.clear()

    def initValues(self):
        """Initialize pos, word and count."""
        self.pos = -1
        self.word = ""
        self.count = 0

    def performRankingNaive(self, index, _minpos):
        """Naive ranking of events, does not consider index."""
        maxWord = ""
        maxCount = 0
        for word in self.fdist:
            value = self.fdist[word]

            if maxCount < value <= self.maxSupport:
                maxWord = str(word)
                maxCount = value

        if maxCount > self.count:
            self.pos = index
            self.word = maxWord
            self.count = maxCount

    def performRankingMeanIndex(self, index, minPos):
        """If two events have the same number of Occurrences tie breake
        based on minimum Mean Index value.
        """
        maxWord = ""
        maxCount = 0

        for word in self.fdist:
            value = self.fdist[word]

            meanPos = sum(self.fdistInd[word]) / len(self.fdistInd[word])

            if maxCount < value <= self.maxSupport:
                maxWord = str(word)
                maxCount = value
                minPos = meanPos

            if value == maxCount and meanPos < minPos:
                maxWord = str(word)
                maxCount = value
                minPos = meanPos

        if maxCount > self.count or (maxCount == self.count and self.pos < index):
            self.pos = index
            self.word = maxWord
            self.count = maxCount

    def performRankingMedianIndex(self, index, minPos):
        """If two events have the same number of Occurrences tie breake
        based on minimum Mean Index value.
        """
        maxWord = ""
        maxCount = 0

        for word in self.fdist:
            value = self.fdist[word]

            meadianPos = np.median(self.fdistInd[word])

            if maxCount < value <= self.maxSupport:
                maxWord = str(word)
                maxCount = value
                minPos = meadianPos

            if value == maxCount and meadianPos < minPos:
                maxWord = str(word)
                maxCount = value
                minPos = meadianPos

        if maxCount > self.count or (maxCount == self.count and self.pos < index):
            self.pos = index
            self.word = maxWord
            self.count = maxCount

    def numberOfSequence(self, evtHashes, startPos, endPos, seq):
        """Choose the event present in maximum number of sequences
        as the next Pattern event.
        """

        duplicate = []
        for j in range(startPos, endPos):
            word = evtHashes[j]
            if word in duplicate:
                continue
            duplicate.append(word)
            if word not in self.fdist:
                self.fdist[word] = seq.getVolume()
                self.fdistInd[word] = [j]
            else:
                self.fdist[word] += seq.getVolume()
                self.fdistInd[word].append(j)

    def allOccurrence(self, evtHashes, startPos, endPos, seq):
        """Choose the event present maximum number of time across sequences
        as the next Pattern event.
        """

        for j in range(startPos, endPos):
            word = evtHashes[j]
            if word not in self.fdist:
                self.fdist[word] = seq.getVolume()
                self.fdistInd[word] = [j]
            else:
                self.fdist[word] += seq.getVolume()
                self.fdistInd[word].append(j)
