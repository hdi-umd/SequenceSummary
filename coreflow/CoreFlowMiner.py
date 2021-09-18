""""Implements the CoreFlow mining Algorithm based on provided Ranking Function"""
from coreflow.RankingFunction import RankingFunction
from Node import TreeNode
from Sequence import Sequence
from Graph import Graph, RawNode, Links


class CoreFlowMiner:
    """Runs Coreflow mining algo"""

    def __init__(self, attribute, minSup, maxSup):
        self.attr = attribute
        self.minSupport = minSup
        self.maxSupport = maxSup

        self.branchSequences = {}
        # FrequencyMedianRankingFunction()
        self.ranker = RankingFunction(self.attr, maxSup)
        self.ranker.setRankingFunc(self.ranker.numberOfSequence)
        self.ranker.setTieBreaker(self.ranker.performRankingMeanIndex)

    def runCoreFlowMiner(self, sequences):
        """Creates a Root Node to start mining."""
        print("Start of all " + str(len(sequences))+" visits")
        root = TreeNode(self.attr, Sequence.getSeqVolume(
            sequences), "Start")
        graph = Graph()
        root.graph = graph
        graph.nodes.append(RawNode(root))
        self.run(sequences, root, graph, exitNodeHash=-1)
        return root, graph

    def run(self, seqs, parent, graph, exitNodeHash):
        """Implement CoreFlow algo which takes a list of sequences, a TreeNode (root),
        the attribute to perform mining on, checkpoints from where to start mining,
        list of events to exclude and other CoreFlow parameters.
        """
        if Sequence.getSeqVolume(seqs) < self.minSupport:
            self.bundleToExit(seqs, parent, graph, exitNodeHash)
            return

        # self.ranker.setEvtAttr(self.attr)
        # print(f'maxval {maxval}')
        # self.ranker.performRanking2(seqs)
        self.ranker.performRanking(seqs)
        topPattern = self.ranker.getTopEventSet()
        print(f'topPattern {topPattern.keyEvts}')

        if topPattern is None:
            print("no patterns found")
            self.bundleToExit(seqs, parent, graph, exitNodeHash)
            return
        containSegs = []
        notContain = []

        node = TreeNode(attr=self.attr)
        node.parent = parent.parent[:]
        node.parent.append(parent)
        hashVal = topPattern.keyEvts[0]
        eVal = seqs[0].getEvtAttrValue(self.attr, hashVal)
        node.setValue(eVal)
        node.setHash(hashVal)
        #node.attr = self.attr
        node.keyevts = parent.keyevts[:]
        node.keyevts.append(hashVal)
        node.sequences = topPattern.sids
        topPattern.computePatternStats(self.attr)
        # if node.parent:
        #     print(node.parent[-1])
        #     print(topPattern.meanPos)
        #     node.meanStep = node.parent[-1].meanStep + topPattern.meanPos[-1]
        #     node.medianPos = node.parent[-1].medianStep + topPattern.medianPos[-1]
        # node.setPositions([Pattern.getPositions(node.keyevts, seq.getHashList(self.attr))[-1]
        #                   for seq in node.sequences])
        node.calcPositionsGenericNode()
        # node.calcPositions()
        # node.calcPositionsAlternate()
        # node.setPositions([pox[-1]-pox[-2]
        # for pox in (Pattern.getPositions(node.keyevts, seq.getHashList(evtAttr))
        # for seq in node.sequences) if len(pox) > 1])

        #print(f'node seqs{node.sequences}')
        #print(f'value {eVal}')
        
        self.truncateSequences(
            seqs, hashVal, node, containSegs, notContain)
        # node.setSeqCount(Sequence.getSeqVolume(containSegs))
        print(f'mean Step {node.meanStep}')
        print(f'seq count {node.getSeqCount()}')
        print([seq.getSeqLen()for seq in containSegs])
        print([seq.sid.getSeqLen()for seq in containSegs])
        print([seq.sid.getEventsString(self.attr)for seq in node.sequences])
        #print(f'seq count {node.getSeqCount()}')

        if node.getSeqCount() >= self.minSupport:
            graph.nodes.append(RawNode(node))
            parent.children.append(node)
            graph.links.append(
                Links(parent, node, node.seqCount, node.meanStep))
            self.run(containSegs, node, graph, exitNodeHash)
            self.run(notContain, parent, graph, exitNodeHash)

        else:
            self.bundleToExit(seqs, parent, graph, exitNodeHash)

    def adjustMin(self, seqs):
        """Adjusts minimum support value."""
        if self.minSupport < 50:
            return self.minSupport

        while(Sequence.getSeqVolume(seqs) < self.minSupport and self.minSupport > 50):
            minval = self.minSupport/2

        return minval

    def truncateSequences(self, seqs, hashVal, node, trailingSeqSegs, notContain):
        """Truncate the sequences based on where current top ranked event is found.
        For example, if current Sequence is ADBC and the top ranked event is D, then
        then the sequence is truncated up to D and the current sequence becomes BC.
        """
        indices = []
        uniqueEvts = []
        incomingBranchSeqs = []

        for seq in seqs:
            ind = seq.getEventPosition(self.attr, hashVal)
            if ind < 0:
                notContain.append(seq)
                print(f'not contain {seq.getHashList(self.attr)}')
            else:
                if ind >= 0:
                    incomingSeq = Sequence(
                        seq.events[0:ind], seq.eventstore, seq.sid)
                    self.branchSequences[incomingSeq.getPathID()] = incomingSeq
                    incomingSeq.setVolume(seq.getVolume())
                    incomingBranchSeqs.append(incomingSeq)
                    print(f'previous {incomingSeq.getHashList(self.attr)}')
                    uniqueEvts.extend(
                        incomingSeq.getUniqueValueHashes(self.attr))

                if len(seq.events)+1 > ind:
                    outgoingSeq = Sequence(
                        seq.events[ind+1:len(seq.events)], seq.eventstore, seq.sid)
                    self.branchSequences[outgoingSeq.getPathID()] = outgoingSeq

                    outgoingSeq.setVolume(seq.getVolume())
                    trailingSeqSegs.append(outgoingSeq)
                    print(f'next {outgoingSeq.getHashList(self.attr)}')

                indices.extend([ind]*(seq.getVolume()))

                print(f'type {seq.events[ind].type}')

        node.setIncomingBranchUniqueEvts(len(set(uniqueEvts)))
        node.setSeqCount(Sequence.getSeqVolume(incomingBranchSeqs))
        # node.setPositions(indices)
        node.setIncomingSequences(incomingBranchSeqs)
        #print(f'seq count {node.getSeqCount()}')
        #print(f'Seq len trailing {len(trailingSeqSegs)}')
        #print(f'Seq len not contain {len(notContain)}')
        #print(f'Seq incoming {node.incomingSequences}')

    def bundleToExit(self, seqs, parent, graph, exitNodeHash):
        """Creates Exit Node as Pattern can not be exended."""
        print(seqs)
        print(parent)
        if len(seqs) == 0:
            return

        node = TreeNode(attr=self.attr)
        node.parent = parent.parent[:]
        node.parent.append(parent)
        #node.attr = self.attr
        node.sequences.extend([seq.sid for seq in seqs])
        print(f'node sequences {node.sequences}')
        print(f'exit node hash {exitNodeHash}')
        if exitNodeHash == -1:
            node.setValue("Exit")
            node.setHash(-2)

        else:
            # set attribute value for this sequence
            node.setValue(seqs[0].getEvtAttrValue(self.attr, exitNodeHash))
            node.setHash(exitNodeHash)

        node.setIncomingSequences(seqs)
        node.setSeqCount(Sequence.getSeqVolume(seqs))
        node.keyevts = parent.keyevts[:]
        print([seq.getSeqLen()for seq in seqs])
        print([seq.sid.getEventsString(self.attr)for seq in seqs])
        print(f'exit node seq count {node.seqCount}')

        # lengths = []
        # for elem in seqs:
        #     lengths.extend([len(elem.sid.events)]
        #                    (elem.sid.getVolume()))
        # for i in range(s.getVolume()):
        #    lengths.append(len(s.events)-1)
        # print(f' len {lengths}')
        node.calcPositionsExitNode()
        # node.calcPositions(isExit=1)
        graph.nodes.append(RawNode(node))
        print(f'mean Step {node.meanStep}')
        parent.children.append(node)
        graph.links.append(
            Links(parent, node, node.seqCount, node.meanStep))
