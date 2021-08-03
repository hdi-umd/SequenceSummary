"""Implements the SentenTreeMiner according to SentenTree Algo"""

import numpy as np
from Graph import RawNode, Links
from TreeNode import GraphNode
from Sequence import Sequence


class SentenTreeMiner:
    """Runs SentenTree mining algo"""

    def __init__(self):
        self.rankingFunc = SentenTreeMiner.numberOfSequence
        self.tieBreaker = SentenTreeMiner.performRankingMedianIndex

    def expandSeqTree(self, attr, rootNode, expandCnt, minSupport, maxSupport, graph):
        """Chooses which branch of the tree to expand next."""
        # if len(rootSeq.eventlist>0):
        expandCnt -= len(rootNode.keyevts)
        seqs = []
        seqs.append(rootNode)
        rootNode.setSeqCount(Sequence.getSeqVolume(rootNode.incomingSequences))
        rootNode.attr = attr
        leafSeqs = []

        graph.nodes.append(RawNode(rootNode))
        while seqs and expandCnt > 0:
            currentSeq = max(seqs, key=lambda x: x.seqCount)
            print(f'seqCount: {currentSeq.seqCount}')

            seq0 = currentSeq.after
            seq1 = currentSeq.before

            print(f'this.pattern currentSeq : {currentSeq.keyevts}')

            if not seq1 and not seq0:
                word, pos, count, seq0, seq1 = self.growSeq(
                    attr, currentSeq, minSupport, maxSupport)
                print(f'event: {word}, pos: {pos}, count: {count}')

                if count < minSupport:
                    leafSeqs.append(currentSeq)
                else:

                    seq1.setHash(word)
                    seq1.setValue(
                        currentSeq.incomingSequences[0].getEvtAttrValue(attr, word))
                    seq1.keyevts = currentSeq.keyevts[:]  # deep copy
                    seq0.keyevts = currentSeq.keyevts[:]

                    seq1.keyevts.insert(pos, word)

            if seq1 and seq1.seqCount >= minSupport:
                expandCnt -= 1
                seqs.append(seq1)
                graph.nodes.append(RawNode(seq1))
                graph.links.append(
                    Links(currentSeq.nid, seq1.nid, seq1.seqCount))

            currentSeq.before = seq1
            currentSeq.after = seq0

            if seq0 and seq0.seqCount >= minSupport:
                seqs.append(seq0)
            print(f'seqCount: {[s.seqCount for s in seqs]}')

            del seqs[seqs.index(currentSeq)]

        return leafSeqs.append(seqs)

    @staticmethod
    def performRankingNaive(fdist, _fdistInd, i, _pos, count, maxSupport, _minpos):
        """Naive ranking of events, does not consider index."""
        maxWord = ""
        maxCount = 0
        for word in fdist.keys():
            value = fdist[word]

            if maxCount < value <= maxSupport:
                maxWord = str(word)
                maxCount = value

        if maxCount > count:
            return i, maxWord, maxCount, True

        return i, maxWord, maxCount, False

    @staticmethod
    def performRankingMeanIndex(fdist, fdistInd, i, pos, count, maxSupport, minPos):
        """If two events have the same number of Occurrences tie breake
        based on minimum Mean Index value.
        """
        maxWord = ""
        maxCount = 0

        for word in fdist.keys():
            value = fdist[word]

            meanPos = sum(fdistInd[word]) / len(fdistInd[word])

            if maxCount < value <= maxSupport:
                maxWord = str(word)
                maxCount = value
                minPos = meanPos

            if value == maxCount and meanPos < minPos:
                maxWord = str(word)
                maxCount = value
                minPos = meanPos

        if maxCount > count or (maxCount == count and pos < i):
            return i, maxWord, maxCount, True

        return i, maxWord, maxCount, False

    @staticmethod
    def performRankingMedianIndex(fdist, fdistInd, i, pos, count, maxSupport, minPos):
        """If two events have the same number of Occurrences tie breake
        based on minimum Mean Index value.
        """
        maxWord = ""
        maxCount = 0

        for word in fdist.keys():
            value = fdist[word]

            meadianPos = np.median(fdistInd[word])

            if maxCount < value <= maxSupport:
                maxWord = str(word)
                maxCount = value
                minPos = meadianPos

            if value == maxCount and meadianPos < minPos:
                maxWord = str(word)
                maxCount = value
                minPos = meadianPos

        if maxCount > count or (maxCount == count and pos < i):
            return i, maxWord, maxCount, True

        return i, maxWord, maxCount, False

    @staticmethod
    def numberOfSequence(fdist, evtHashes, startPos, endPos, seq, fdistInd=None):
        """Choose the event present in maximum number of sequences
        as the next Pattern event.
        """

        if fdistInd is None:
            fdistInd = {}
        duplicate = []
        for j in range(startPos, endPos):
            word = evtHashes[j]
            # print(word)
            if word in duplicate:
                continue
            duplicate.append(word)
            if word not in fdist:
                fdist[word] = seq.getVolume()
                fdistInd[word] = [j]
            else:
                fdist[word] += seq.getVolume()
                fdistInd[word].append(j)

    @staticmethod
    def allOccurrence(fdist, evtHashes, startPos, endPos, seq, fdistInd=None):
        """Choose the event present maximum number of time across sequences
        as the next Pattern event.
        """

        if fdistInd is None:
            fdistInd = {}

        for j in range(startPos, endPos):
            word = evtHashes[j]
            # print(word)
            if word not in fdist:
                fdist[word] = seq.getVolume()
                fdistInd[word] = [j]
            else:
                fdist[word] += seq.getVolume()
                fdistInd[word].append(j)

    def growSeq(self, attr, seq, minSupport, maxSupport):
        """Expands the current max Pattern by another event."""
        pos = -1
        word = ""
        count = 0

        for i in range(0, len(seq.keyevts)+1):
            fdist = {}
            fdistInd = {}

            for elem in seq.incomingSequences:

                evtHashes = elem.getHashList(attr)
                startPos = 0 if i == 0 else elem.seqIndices[i - 1] + 1
                endPos = len(evtHashes) if i == len(
                    seq.keyevts) else elem.seqIndices[i]

                self.rankingFunc(fdist, evtHashes, startPos,
                                 endPos, elem, fdistInd)

            minPos = max(len(x.events) for x in seq.incomingSequences)

            newPos, newWord, newCount, verdict = self.tieBreaker(
                fdist, fdistInd, i, pos, count, maxSupport, minPos)

            if verdict:
                pos = newPos
                word = newWord
                count = newCount

        seq0 = GraphNode(attr=attr)
        seq1 = GraphNode(attr=attr)

        if count >= minSupport:
            words = seq.keyevts
            for elem in seq.incomingSequences:
                startPos = 0 if pos == 0 else elem.seqIndices[pos - 1] + 1
                endPos = len(elem.events) if pos == len(
                    words) else elem.seqIndices[pos]
                try:
                    i = elem.getHashList(attr).index(word, startPos, endPos)
                    # sequence index value for the word being inserted. e.g. A-C-G seq indice 1,4,8
                    elem.seqIndices.insert(pos, i)
                    seq1.incomingSequences.append(elem)
                    seq1.seqCount += elem.getVolume()

                except ValueError:
                    seq0.incomingSequences.append(elem)
                    seq0.seqCount += elem.getVolume()
            # calculate average index
            posArr = [seq.seqIndices[pos] for seq in seq1.incomingSequences]
            seq1.setPositions(posArr)
            seq0.setSeqCount(Sequence.getSeqVolume(seq0.incomingSequences))
            seq1.setSeqCount(Sequence.getSeqVolume(seq1.incomingSequences))

            print(f'Not contain: {len(seq0.incomingSequences)}')
            print(f'contain: {len(seq1.incomingSequences)}')
        return word, pos, count, seq0, seq1
