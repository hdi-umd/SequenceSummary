"""Implements the SentenTreeMiner according to SentenTree Algo."""

import numpy as np
from Graph import RawNode, Graph
from Node import GraphNode
from Sequence import Sequence
from sententree.RankingFunction import RankingFunction


class SentenTreeMiner:
    """Runs SentenTree mining algo"""

    def __init__(self, attribute, minSup, maxSup):
        self.attr = attribute
        self.minSupport = minSup
        self.maxSupport = maxSup
        self.ranker = RankingFunction(maxSup)
        self.ranker.setRankingFunc(self.ranker.numberOfSequence)
        self.ranker.setTieBreaker(self.ranker.performRankingMedianIndex)

    def runSentenTreeMiner(self, sequences):
        """Run the sentenTreeMiner algorithm in the given sequences."""
        GraphNode.resetCounter()
        root = GraphNode(self.attr, Sequence.getSeqVolume(sequences), "_Start")
        root.sequences = sequences
        root.graph = Graph()
        graph = self.expandSeqTree(root, expandCnt=100)
        return graph

    def expandSeqTree(self, rootNode, expandCnt, graphs=None):
        """Chooses which branch of the tree to expand next."""

        if not graphs:
            graphs = []
        expandCnt -= len(rootNode.keyevts)
        seqs = []
        seqs.append(rootNode)
        #rootNode.setSeqCount(Sequence.getSeqVolume(rootNode.sequences))
        #rootNode.attr = self.attr
        rootNode.parent.append(rootNode)

        leafSeqs = []

        rootNode.graph.nodes.append(RawNode(node=rootNode))
        graphs.append(rootNode.graph)
        while seqs and expandCnt > 0:
            currentSeq = max(seqs, key=lambda x: x.seqCount)

            graph = currentSeq.graph

            seq0 = currentSeq.after
            seq1 = currentSeq.before

            if not seq1 and not seq0:
                word, pos, count, seq0, seq1 = self.growSeq(currentSeq)
                #print(f'key event {word} inserted at {pos} with count {count}')
                #print(f'nid {seq1.nid}')
                if count <= self.minSupport:
                    #currentSeq.parent.insert(0, rootNode)
                    leafSeqs.append(currentSeq)
                else:
                    if not graph:
                        graph = Graph()
                        graphs.append(graph)

                    seq1.setHash(word)
                    seq1.setValue(
                        currentSeq.sequences[0].getEvtAttrValue(self.attr, word))
                    seq0.keyevts = currentSeq.keyevts[:]
                    seq1.keyevts = currentSeq.keyevts[:]  # deep copy
                    seq1.keyevts.insert(pos, word)

                    seq0.parent = currentSeq.parent[:]
                    seq1.parent = currentSeq.parent[:]
                    # seq1.calcPositionsGenericNode()
                    seq1.parent.insert(pos+1, seq1)
                    # seq0.parent.append(seq0.nid)

                    seq0.meanStep = currentSeq.meanStep
                    seq0.medianStep = currentSeq.medianStep
                    seq0.graph = currentSeq.graph
                    seq1.graph = graph

            currentSeq.before = seq1
            currentSeq.after = seq0

            if seq1 and seq1.seqCount >= self.minSupport:
                expandCnt -= 1
                seqs.append(seq1)
                graph.nodes.append(RawNode(node=seq1, pos=pos))

            if seq0 and seq0.seqCount >= self.minSupport:
                seqs.append(seq0)

            del seqs[seqs.index(currentSeq)]

        leafSeqs.extend(seqs)

        for seq in leafSeqs:
            exitNode = GraphNode(self.attr)
            exitNode.value = "_Exit"
            exitNode.seqCount = seq.seqCount
            exitNode.sequences = seq.sequences
            exitNode.keyevts = seq.keyevts[:]
            exitNode.parent = seq.parent[:]
            # exitNode.parent.append(seq)
            # exitNode.calcPositionsExitNode()
            exitNode.before = seq
            seq.after = exitNode
            lenArr = [len(x.events) for x in seq.sequences]
            exitNode.meanStep = sum(lenArr)/len(lenArr)
            exitNode.medianStep = np.median(lenArr)
            # exitNode.parent.append(seq)
            seq.parent.append(exitNode)

            seq.graph.nodes.append(RawNode(node=exitNode, pos=-1))

        self.updateNodesEdges(graphs, leafSeqs)
        for graph in graphs:
            graph.createLinks()
            graph.detectCycles()
            # uses max predecessor
            #graph.calcPositionsNodeMaxPredecessor()
            # uses first node
            graph.calcPositionsNode()
            graph.calcLengthsLink()
            # graph.bundle()
        newGraph = Graph.assembleGraphs(graphs)

        return newGraph

    def growSeq(self, seq):
        """Expands the current max Pattern by another event."""
        self.ranker.initValues()

        for i in range(0, len(seq.keyevts)+1):
            self.ranker.clearfdists()

            for elem in seq.sequences:

                evtHashes = elem.getHashList(self.attr)
                startPos = 0 if i == 0 else elem.seqIndices[i - 1] + 1
                endPos = len(evtHashes) if i == len(
                    seq.keyevts) else elem.seqIndices[i]

                self.ranker.rankingFunc(evtHashes, startPos,
                                        endPos, elem)

            minPos = max(len(x.events) for x in seq.sequences)

            self.ranker.tieBreaker(i, minPos)

        seq0 = GraphNode(attr=self.attr)
        seq1 = GraphNode(attr=self.attr)

        if self.ranker.count >= self.minSupport:
            words = seq.keyevts
            seqIds = []
            for elem in seq.sequences:
                startPos = 0 if self.ranker.pos == 0 else elem.seqIndices[self.ranker.pos - 1] + 1
                endPos = len(elem.events) if self.ranker.pos == len(
                    words) else elem.seqIndices[self.ranker.pos]
                try:
                    i = elem.getHashList(self.attr).index(
                        self.ranker.word, startPos, endPos)
                    # sequence index value for the word being inserted. e.g. A-C-G seq indice 1,4,8
                    elem.seqIndices.insert(self.ranker.pos, i)
                    seq1.sequences.append(elem)
                    seq1.seqCount += elem.getVolume()
                    seqIds.append(elem._id)

                except ValueError:
                    seq0.sequences.append(elem)
                    seq0.seqCount += elem.getVolume()
            # calculate average index
            posArr = [seq.seqIndices[self.ranker.pos]
                      for seq in seq1.sequences]
            #print(f'Sequence id {seqIds}')
            seq1.setPositions(posArr)
            seq0.setSeqCount(Sequence.getSeqVolume(seq0.sequences))
            seq1.setSeqCount(Sequence.getSeqVolume(seq1.sequences))

            #print(f'Not contain: {len(seq0.sequences)}')
            #print(f'contain: {len(seq1.sequences)}')

        return self.ranker.word, self.ranker.pos, self.ranker.count, seq0, seq1

    @staticmethod
    def updateNodesEdges(graphs, leafSeqs):
        """Assign edge weights, update which node is connected to which."""
        for seq in leafSeqs:
            linkadj = seq.graph.linkAdj

            if seq.graph in graphs:

                for first, second in zip(seq.parent, seq.parent[1:]):
                    if first.nid not in linkadj:
                        linkadj[first.nid] = {}
                    if second in linkadj[first.nid]:
                        linkadj[first.nid][second.nid] += min(
                            first.seqCount, second.seqCount)
                    else:
                        linkadj[first.nid][second.nid] = min(
                            first.seqCount, second.seqCount)
            #print(linkadj)
