"""Implements the sequence synopsis mining class."""

from collections import Counter
from bisect import bisect
import math
from sequence_summary.core.cluster import Cluster
from sequence_summary.mining.sequencesynopsis.ranking_function import (
    lcs,
    calcDist,
    calcAverage,
)
from sequence_summary.core.queue_elements import QueueElements
from sequence_summary.core.pattern import Pattern
from datasketch import MinHash, MinHashLSH, WeightedMinHashGenerator
from sklearn.feature_extraction.text import TfidfVectorizer
from sequence_summary.core.graph import Graph, RawNode, Links


class SequenceSynopsisMiner:
    """Based on some metric distance, groups sequences under same pattern."""

    def __init__(self, attrib, evtStore, alpha=0.1, lambdaVal=0.9):
        self.attr = attrib
        self.eventStore = evtStore
        self.alpha = alpha
        self.lambdaVal = lambdaVal
        self.clustDict = []  # To-Do: Make clustDict class var
        RawNode.resetCounter()

    def createMinHashandLSH(self, threshold):
        """
        Input: clustDict: Doctionary of clusters
        threshold: float value of threshold
        Returns a minHashArr and the LSH arr
        """
        vectorizer = TfidfVectorizer(
            token_pattern=r"\w+", norm="l1", sublinear_tf=True, use_idf=False
        )

        for val in self.clustDict:
            patStrings = [
                " ".join(
                    str(self.eventStore.getEventValue(self.attr, val.pattern.keyEvts))
                )
                for val in self.clustDict
            ]

        vectors = vectorizer.fit_transform(patStrings)
        dense = vectors.todense()
        denselist = dense.tolist()
        # Cluster.printClustDict(clustDict, self.attr)
        wmg = WeightedMinHashGenerator(len(denselist[0]))

        minHashArr = []
        lsh = MinHashLSH(threshold=threshold)
        for ind, val in enumerate(denselist):
            minHashArr.append(wmg.minhash(val))
            lsh.insert(self.clustDict[ind], minHashArr[ind])
        return lsh, minHashArr

    def minDL(self, seqs):
        """Merges sequences based on minimum Description Length."""
        # Initialization Phase
        thStart = 0.9
        thEnd = 0.2
        thRate = 0.6
        self.clustDict = [
            Cluster(
                Pattern(seq.getHashList(self.attr)),
                [seq],
                list(range(0, seq.getSeqLen())),
            )
            for seq in seqs
        ]
        priorityQueue = []

        threshold = thStart
        while threshold > thEnd:
            lsh, minHashArr = self.createMinHashandLSH(threshold)
            for i, clust1 in enumerate(self.clustDict):
                for j, clust2 in enumerate(lsh.query(minHashArr[i])):
                    if clust1 == clust2:
                        continue
                    deltaL, cStar = self.merge(clust1, clust2)
                    # print(f'returned {deltaL}, {cStar}')
                    if deltaL > 0:
                        priorityQueue.append(
                            QueueElements(deltaL, cStar, clust1, clust2)
                        )

            # QueueElements.printPriorityQueue(priorityQueue, self.attr)
            while priorityQueue:
                priorityQueue = sorted(
                    priorityQueue, key=lambda x: x.deltaL, reverse=True
                )  # sort on deltaL

                # print(f'to Merge ')
                toMerge = priorityQueue[0]
                # print(toMerge.clust1)
                # print(toMerge.clust2)
                # print(clustDict)
                cNew = toMerge.cStar
                self.clustDict.remove(toMerge.clust1)
                self.clustDict.remove(toMerge.clust2)
                self.clustDict.append(cNew)

                deleteIndices = []

                for val, entries in enumerate(priorityQueue):
                    if (
                        toMerge.clust1.pattern == entries.clust1.pattern
                        or toMerge.clust2.pattern == entries.clust1.pattern
                    ):
                        deleteIndices.append(val)
                    elif (
                        toMerge.clust1.pattern == entries.clust2.pattern
                        or toMerge.clust2.pattern == entries.clust2.pattern
                    ):
                        deleteIndices.append(val)

                for index in sorted(deleteIndices, reverse=True):
                    del priorityQueue[index]

                lsh, minHashArr = self.createMinHashandLSH(threshold)

                for clus in lsh.query(minHashArr[-1]):
                    if clus == cNew:
                        continue
                    deltaL, cStar = self.merge(clus, cNew)
                    if deltaL > 0:
                        priorityQueue.append(QueueElements(deltaL, cStar, clus, cNew))
                # QueueElements.printPriorityQueue(priorityQueue, self.attr)
            threshold = threshold * thRate
            # print(threshold)
        grph = self.transformToGraph(self.clustDict)
        return self.clustDict, grph

    def merge(self, pair1, pair2):
        """Merge two seqLists and calculate the description length reduction"""
        pStar = Pattern(lcs(pair1.pattern.keyEvts, pair2.pattern.keyEvts))
        candidateEvents = list(
            (
                (Counter(pair1.pattern.keyEvts) - Counter(pStar.keyEvts))
                | (Counter(pair2.pattern.keyEvts) - Counter(pStar.keyEvts))
            ).elements()
        )
        if not candidateEvents:
            # same pattern
            clust = Cluster(
                pStar, pair1.seqList + pair2.seqList, list(range(len(pStar.keyEvts)))
            )
            return 100, clust
        candidateEventsCounter = Counter(candidateEvents)
        candidateEventsCounter = sorted(
            candidateEventsCounter, key=candidateEventsCounter.get, reverse=True
        )

        deltaL = -1
        # print(f'p1 {pair1.pattern.keyEvts}')
        # print(f'p2 {pair2.pattern.keyEvts}')

        lcsPosPat1 = Pattern.getPositions(pStar.keyEvts, pair1.pattern.keyEvts)
        lcsPosPat2 = Pattern.getPositions(pStar.keyEvts, pair2.pattern.keyEvts)
        averagePos = calcAverage(lcsPosPat1, lcsPosPat2)
        # print(f'Average Pos {averagePos}')

        # print(f'candidates {candidateEventsCounter}')
        clust = Cluster(pStar, pair1.seqList + pair2.seqList, averagePos)
        selectedIndex = -1

        for candidate in candidateEventsCounter:
            deltaLArr = []
            pStarArr = []
            indexArr = []
            indicesKey1 = [
                i for i, x in enumerate(pair1.pattern.keyEvts) if x == candidate
            ]
            indicesKey2 = [
                i for i, x in enumerate(pair2.pattern.keyEvts) if x == candidate
            ]
            candidatePos = []

            # Find in which indices current candidate event could be inserted
            for ind in indicesKey1:
                if candidate in pStar.keyEvts and ind in lcsPosPat1:
                    # event already in LCS
                    continue
                index = bisect(lcsPosPat1, ind)
                candidatePos.append(index)

            for ind in indicesKey2:
                if candidate in pStar.keyEvts and ind in lcsPosPat2:
                    continue
                index = bisect(lcsPosPat2, ind)
                candidatePos.append(index)

            candidatePos = list(set(candidatePos))
            # print(f'candidatepos {candidatePos}')
            tempPattern = Pattern(pStar.keyEvts[:])
            for index in candidatePos:
                tempPattern.keyEvts.insert(index, candidate)
                # print(f'index {index}')
                deltaLPrime = (
                    len(pair1.pattern.keyEvts)
                    + len(pair2.pattern.keyEvts)
                    - len(tempPattern.keyEvts)
                    + self.lambdaVal
                )
                # print(f'del L Prime  {deltaLPrime}')
                deltaLPrime += sum(
                    self.alpha
                    * calcDist(v1.getHashList(self.attr), pair1.pattern.keyEvts)
                    for v1 in pair1.seqList
                )
                # print(f'del L Prime  {deltaLPrime}')
                deltaLPrime += sum(
                    self.alpha
                    * calcDist(v2.getHashList(self.attr), pair2.pattern.keyEvts)
                    for v2 in pair2.seqList
                )

                deltaLPrime -= sum(
                    self.alpha * calcDist(v.getHashList(self.attr), tempPattern.keyEvts)
                    for v in pair1.seqList + pair2.seqList
                )

                if deltaLPrime < 0 or deltaLPrime < deltaL:
                    del tempPattern.keyEvts[index]
                    continue

                deltaLArr.append(deltaLPrime)
                pStarArr.append(Pattern(tempPattern.keyEvts[:]))
                indexArr.append(index)

                # index calculation
                del tempPattern.keyEvts[index]
            if deltaLArr:
                if max(deltaLArr) > deltaL:
                    deltaL = max(deltaLArr)
                    maxInd = deltaLArr.index(max(deltaLArr))
                    selectedIndex = indexArr[maxInd]
                    pStar = pStarArr[maxInd]
                    if selectedIndex != -1:
                        if selectedIndex == 0:
                            averagePos.insert(0, 0)
                        if selectedIndex >= len(averagePos):
                            averagePos.append(averagePos[-1] + 1)
                        else:
                            averagePos.insert(
                                selectedIndex,
                                (
                                    averagePos[selectedIndex - 1]
                                    + averagePos[selectedIndex]
                                )
                                / 2.0,
                            )
                    clust = Cluster(pStar, pair1.seqList + pair2.seqList, averagePos)

        return deltaL, clust

    def transformToGraph(self, clust):
        """Given a list of clusters, convert this to graph."""
        graph = Graph()
        count = 0
        for index, elem in enumerate(clust):
            keyEvents = self.eventStore.getEventValue(self.attr, elem.pattern.keyEvts)
            # Start
            node = RawNode()
            node.seqCount = str(len(elem.seqList))
            node.value = "_Start"
            node.pos = 0
            node.sequences = elem.seqList
            node.attr = self.attr
            node.pattern = index
            parentList = [node]
            graph.nodes.append(node)
            count += 1
            for ind, event in enumerate(elem.pattern.keyEvts):
                node = RawNode()
                node.seqCount = str(len(elem.seqList))
                node.value = keyEvents[ind]
                node.pos = ind
                node.keyevts = elem.pattern.keyEvts
                node.pattern = index
                node.parent = parentList

                # node.pattern = " ".join(self.eventStore.getEventValue(
                #     self.attr, elem.pattern.keyEvts[:ind+1]))
                node.sequences = elem.seqList
                node.attr = self.attr
                node.meanStep = -1
                node.medianStep = -1
                parentList.append(node)
                graph.nodes.append(node)

                # This means not the first node of Pattern

                graph.links.append(
                    Links(graph.nodes[count - 1], graph.nodes[count], len(elem.seqList))
                )
                # graph.calcLengthsLink()
                count += 1
            # Exit Node
            node = RawNode()
            node.seqCount = str(len(elem.seqList))
            node.value = "_Exit"
            node.pos = ind + 1
            node.sequences = elem.seqList
            node.attr = self.attr
            node.pattern = index
            node.parent = parentList
            node.keyevts = elem.pattern.keyEvts
            graph.nodes.append(node)
            graph.links.append(
                Links(graph.nodes[count - 1], graph.nodes[count], len(elem.seqList))
            )
            count += 1

            graph.calcPositionsNode(matchAll=False)
            graph.getEventValueForNodes()
        return graph
