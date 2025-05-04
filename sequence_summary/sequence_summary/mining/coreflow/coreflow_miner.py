""" "Implements the CoreFlow mining Algorithm based on provided Ranking Function"""

from sequence_summary.mining.coreflow.ranking_function import RankingFunction
from sequence_summary.core.node import TreeNode
from sequence_summary.datamodel.sequence import Sequence
from sequence_summary.core.graph import Graph, RawNode, Links


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
        TreeNode.resetCounter()
        root = TreeNode(self.attr, Sequence.getSeqVolume(sequences), "_Start")

        graph = Graph()
        root.graph = graph
        graph.nodes.append(RawNode(node=root, isCoreflow=True))
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
        # self.ranker.performRanking2(seqs)
        self.ranker.performRanking(seqs)
        topPattern = self.ranker.getTopEventSet()

        if topPattern is None:
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
        # node.attr = self.attr
        node.keyevts = parent.keyevts[:]
        node.keyevts.append(hashVal)
        node.sequences = topPattern.sids
        topPattern.computePatternStats(self.attr)
        # if node.parent:
        #     node.meanStep = node.parent[-1].meanStep + topPattern.meanPos[-1]
        #     node.medianPos = node.parent[-1].medianStep + topPattern.medianPos[-1]
        # node.setPositions([Pattern.getPositions(node.keyevts, seq.getHashList(self.attr))[-1]
        #                   for seq in node.sequences])
        linkLength = node.calcPositionsGenericNode()
        # node.calcPositions()
        # node.calcPositionsAlternate()
        # node.setPositions([pox[-1]-pox[-2]
        # for pox in (Pattern.getPositions(node.keyevts, seq.getHashList(evtAttr))
        # for seq in node.sequences) if len(pox) > 1])

        self.truncateSequences(seqs, hashVal, node, containSegs, notContain)
        # node.setSeqCount(Sequence.getSeqVolume(containSegs))

        if node.getSeqCount() >= self.minSupport:
            graph.nodes.append(RawNode(node=node, isCoreflow=True))
            parent.children.append(node)
            graph.links.append(Links(parent, node, node.seqCount, linkLength))
            self.run(containSegs, node, graph, exitNodeHash)
            self.run(notContain, parent, graph, exitNodeHash)

        else:
            self.bundleToExit(seqs, parent, graph, exitNodeHash)

    def adjustMin(self, seqs):
        """Adjusts minimum support value."""
        if self.minSupport < 50:
            return self.minSupport

        while Sequence.getSeqVolume(seqs) < self.minSupport and self.minSupport > 50:
            minval = self.minSupport / 2

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
            else:
                if ind >= 0:
                    incomingSeq = Sequence(seq.events[0:ind], seq.eventstore, seq.sid)
                    self.branchSequences[incomingSeq.getPathID()] = incomingSeq
                    incomingSeq.setVolume(seq.getVolume())
                    incomingBranchSeqs.append(incomingSeq)
                    uniqueEvts.extend(incomingSeq.getUniqueValueHashes(self.attr))

                if len(seq.events) + 1 > ind:
                    outgoingSeq = Sequence(
                        seq.events[ind + 1 : len(seq.events)], seq.eventstore, seq.sid
                    )
                    self.branchSequences[outgoingSeq.getPathID()] = outgoingSeq

                    outgoingSeq.setVolume(seq.getVolume())
                    trailingSeqSegs.append(outgoingSeq)

                indices.extend([ind] * (seq.getVolume()))

        node.setIncomingBranchUniqueEvts(len(set(uniqueEvts)))
        node.setSeqCount(Sequence.getSeqVolume(incomingBranchSeqs))
        # node.setPositions(indices)
        node.setIncomingSequences(incomingBranchSeqs)

    def bundleToExit(self, seqs, parent, graph, exitNodeHash):
        """Creates Exit Node as Pattern can not be exended."""
        if len(seqs) == 0:
            return

        node = TreeNode(attr=self.attr)
        node.parent = parent.parent[:]
        node.parent.append(parent)
        # node.attr = self.attr
        node.sequences.extend([seq.sid for seq in seqs])
        if exitNodeHash == -1:
            node.setValue("_Exit")
            node.setHash(-2)

        else:
            # set attribute value for this sequence
            node.setValue(seqs[0].getEvtAttrValue(self.attr, exitNodeHash))
            node.setHash(exitNodeHash)

        node.setIncomingSequences(seqs)
        node.setSeqCount(Sequence.getSeqVolume(seqs))
        node.keyevts = parent.keyevts[:]

        # lengths = []
        # for elem in seqs:
        #     lengths.extend([len(elem.sid.events)]
        #                    (elem.sid.getVolume()))
        # for i in range(s.getVolume()):
        #    lengths.append(len(s.events)-1)
        linkLength = node.calcPositionsExitNode()
        # node.calcPositions(isExit=1)
        graph.nodes.append(RawNode(node=node, isCoreflow=True))
        parent.children.append(node)
        graph.links.append(Links(parent, node, node.seqCount, linkLength))
