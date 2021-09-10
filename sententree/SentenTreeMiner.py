"""Implements the SentenTreeMiner according to SentenTree Algo"""

from Graph import RawNode, Graph
from Node import GraphNode
from Sequence import Sequence
from sententree.RankingFunction import RankingFunction
import numpy as np

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
        root = GraphNode()
        root.incomingSequences = sequences
        root.graph = Graph()
        graph = self.expandSeqTree(root, expandCnt=100)
        return graph

    def expandSeqTree(self, rootNode, expandCnt, graphs=None):
        """Chooses which branch of the tree to expand next."""
        # if len(rootSeq.eventlist>0):
        if not graphs:
            graphs = []
        expandCnt -= len(rootNode.keyevts)
        seqs = []
        seqs.append(rootNode)
        rootNode.setSeqCount(Sequence.getSeqVolume(rootNode.incomingSequences))
        rootNode.attr = self.attr
        rootNode.parent.append(rootNode.nid)
        leafSeqs = []

        rootNode.graph.nodes.append(RawNode(rootNode))
        graphs.append(rootNode.graph)
        while seqs and expandCnt > 0:
            currentSeq = max(seqs, key=lambda x: x.seqCount)
            print(f'seqCount: {currentSeq.seqCount}')
            graph = currentSeq.graph

            seq0 = currentSeq.after
            seq1 = currentSeq.before

            #print(f'this.pattern currentSeq : {currentSeq.keyevts}')

            if not seq1 and not seq0:
                word, pos, count, seq0, seq1 = self.growSeq(currentSeq)
                #print(f'event: {word}, pos: {pos}, count: {count}')

                if count <= self.minSupport:
                    leafSeqs.append(currentSeq)
                else:
                    if not graph:
                        graph = Graph()
                        graphs.append(graph)
                        #print(f'\n\n LEN {len(graphs)}\n\n')

                    seq1.setHash(word)
                    seq1.setValue(
                        currentSeq.incomingSequences[0].getEvtAttrValue(self.attr, word))
                    seq1.keyevts = currentSeq.keyevts[:]  # deep copy
                    seq0.keyevts = currentSeq.keyevts[:]
                    seq1.keyevts.insert(pos, word)

                    seq0.parent = currentSeq.parent[:]
                    seq1.parent = currentSeq.parent[:]
                    seq1.parent.insert(pos, seq1.nid)
                    # seq0.parent.append(seq0.nid)

                    seq0.graph = currentSeq.graph
                    seq1.graph = graph

                    linkadj = seq1.graph.linkAdj

                    if len(seq1.parent) > 1:
                        if seq1.parent[pos-1] not in linkadj:
                            linkadj[seq1.parent[pos-1]] = {}
                        if seq1.parent[pos] in linkadj[seq1.parent[pos-1]]:
                            linkadj[seq1.parent[pos-1]
                                    ][seq1.parent[pos]] += seq1.seqCount
                        else:
                            linkadj[seq1.parent[pos-1]
                                    ][seq1.parent[pos]] = seq1.seqCount

            currentSeq.before = seq1
            currentSeq.after = seq0

            if seq1 and seq1.seqCount >= self.minSupport:
                expandCnt -= 1
                seqs.append(seq1)

                graph.nodes.append(RawNode(seq1))

            if seq0 and seq0.seqCount >= self.minSupport:
                seqs.append(seq0)
                #graph.nodes.append(RawNode(seq0, pos))
                # graph.nodes[-1].value = -2  # dummy node value

                # graph.links.append(
                #     Links(currentSeq.nid, seq0.nid, seq0.seqCount))

            #print(f'seqCount: {[s.seqCount for s in seqs]}')

            del seqs[seqs.index(currentSeq)]
            #print(f'Prev pos {prevPos}')

        # for graph in graphs:
        #    graph.collapseNode()
        #    graph.allignNodes()
        leafSeqs.extend(seqs)
        print(f'lrn {len(leafSeqs)}')
        print(f'lrn graph {len(graphs)}')
        
        #self.updateNodesEdges(graphs, leafSeqs)
        for seq in leafSeqs:
            print(seq.graph.linkAdj)
            exitNode = RawNode()
            exitNode.nid = seq.graph.nodes[-1].nid+1
            exitNode.value = -2
            exitNode.seqCount = seq.seqCount
            exitNode.pattern = ""
            lenArr = [len(x.events) for x in seq.incomingSequences]
            exitNode.meanStep = sum(lenArr)/len(lenArr)
            exitNode.medianStep = np.median(lenArr)
            seq.graph.nodes.append(exitNode)
            if seq.nid not in linkadj:
                seq.graph.linkAdj[seq.nid] = {}
                seq.graph.linkAdj[seq.nid][exitNode.nid] = seq.seqCount

        for graph in graphs:
            # print(graph.linkadj)
            graph.createLinks()
            graph.bundle()
        newGraph = Graph.assembleGraphs(graphs)
        #print(f'len {len(graphs)}')
        return newGraph

    def growSeq(self, seq):
        """Expands the current max Pattern by another event."""
        self.ranker.initValues()

        for i in range(0, len(seq.keyevts)+1):
            self.ranker.clearfdists()

            for elem in seq.incomingSequences:

                evtHashes = elem.getHashList(self.attr)
                startPos = 0 if i == 0 else elem.seqIndices[i - 1] + 1
                endPos = len(evtHashes) if i == len(
                    seq.keyevts) else elem.seqIndices[i]

                self.ranker.rankingFunc(evtHashes, startPos,
                                        endPos, elem)

            minPos = max(len(x.events) for x in seq.incomingSequences)

            self.ranker.tieBreaker(i, minPos)

        seq0 = GraphNode(attr=self.attr)
        seq1 = GraphNode(attr=self.attr)

        if self.ranker.count >= self.minSupport:
            words = seq.keyevts
            for elem in seq.incomingSequences:
                startPos = 0 if self.ranker.pos == 0 else elem.seqIndices[self.ranker.pos - 1] + 1
                endPos = len(elem.events) if self.ranker.pos == len(
                    words) else elem.seqIndices[self.ranker.pos]
                try:
                    i = elem.getHashList(self.attr).index(
                        self.ranker.word, startPos, endPos)
                    # sequence index value for the word being inserted. e.g. A-C-G seq indice 1,4,8
                    elem.seqIndices.insert(self.ranker.pos, i)
                    seq1.incomingSequences.append(elem)
                    seq1.seqCount += elem.getVolume()

                except ValueError:
                    seq0.incomingSequences.append(elem)
                    seq0.seqCount += elem.getVolume()
            # calculate average index
            posArr = [seq.seqIndices[self.ranker.pos]
                      for seq in seq1.incomingSequences]
            seq1.setPositions(posArr)
            seq0.setSeqCount(Sequence.getSeqVolume(seq0.incomingSequences))
            seq1.setSeqCount(Sequence.getSeqVolume(seq1.incomingSequences))
            seq0.sequences = seq0.incomingSequences
            seq1.sequences = seq1.incomingSequences

            #print(f'Not contain: {len(seq0.incomingSequences)}')
            #print(f'contain: {len(seq1.incomingSequences)}')

        return self.ranker.word, self.ranker.pos, self.ranker.count, seq0, seq1

    @staticmethod
    def updateNodesEdges(graphs, leafSeqs, countArr):
        """Assign edge weights, update which node is connected to which."""
        i = 0
        for seq in leafSeqs:
            linkadj = seq.graph.linkAdj

            if seq.graph in graphs:
                parents = seq.parent
                print(f'Parents {parents}')
                for first, second in zip(seq.parent, seq.parent[1:]):
                    print(f'seqcount {seq.seqCount}')
                    if first not in linkadj:
                        linkadj[first] = {}
                    if second in linkadj[first]:
                        linkadj[first][second] += countArr[i]
                    else:
                        linkadj[first][second] = countArr[i]
            print(linkadj)
