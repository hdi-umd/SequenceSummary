""""Implements the CoreFlow mining Algorithm based on provided Ranking Function"""

from FrequencyMedianRankingFunction import FrequencyMedianRankingFunction
from OccurrencesMeanRankingFunction import OcccurrencesMeanRankingFunction
from FrequencyMeanRankingFunction import FrequencyMeanRankingFunction
from OccurrencesMedianRankingFunction import OcccurrencesMedianRankingFunction
from TreeNode import TreeNode
from Sequence import Sequence


class CoreFlowMiner:
    """Runs Coreflow mining algo"""

    def __init__(self):
        self.branchSequences = {}
        self.rankingFunc = FrequencyMedianRankingFunction()

    @staticmethod
    def adjustMin(seqs, minval):
        """Adjusts minimum support value."""
        if minval < 50:
            return minval

        while(Sequence.getSeqVolume(seqs) < minval and minval > 50):
            minval = minval/2

        return minval

    @staticmethod
    def bundleToExit(seqs, parent, attr, exitNodeHash):
        """Creates Exit Node as Pattern can not be exended."""
        if len(seqs) == 0:
            return

        node = TreeNode()
        print(f'exit node hash {exitNodeHash}')
        if exitNodeHash == -1:
            node.setName("Exit")
            node.setValue("Exit")
            node.setHash(-2)

        else:
            node.setName(str(seqs[0].getEvtAttrValue(attr, exitNodeHash)))
            # set attribute value for this sequence
            # node.setValue(seqs[0].getEvtAttrValue(attr, exitNodeHash))
            node.setHash(exitNodeHash)

        node.setIncomingSequences(seqs)
        node.setSeqCount(Sequence.getSeqVolume(seqs))
        print(f'exit node seq count {node.seqCount}')
        lengths = []
        for elem in seqs:
            lengths.extend([(len(elem.events)-1)
                            for i in range(elem.getVolume())])
            # for i in range(s.getVolume()):
            #    lengths.append(len(s.events)-1)
        node.setPositions(lengths)
        parent.children.append(node)

    # needs properimplementation
    @staticmethod
    def getNewRootNode(numPaths, seqlist, attr):
        """Creates a Root Node to start mining."""
        print("Start of all " + str(len(seqlist))+" visits")
        return TreeNode("root", numPaths, "Start", attr)

    def truncateSequences(self, seqs, hashVal, evtAttr, node, trailingSeqSegs, notContain):
        """Truncate the sequences based on where current top ranked event is found.
        For example, if current Sequence is ADBC and the top ranked event is D, then
        then the sequence is truncated up to D and the current sequence becomes BC.
        """
        indices = []
        uniqueEvts = []
        relTimestamps = []
        incomingBranchSeqs = []

        for seq in seqs:
            ind = seq.getEventPosition(evtAttr, hashVal)
            if ind < 0:
                notContain.append(seq)
                print(f'not contain {seq.getHashList(evtAttr)}')
            else:
                if ind >= 1:
                    incomingSeq = Sequence(seq.events[0:ind], seq.eventstore)
                    self.branchSequences[incomingSeq.getPathID()] = incomingSeq
                    incomingSeq.setVolume(seq.getVolume())
                    incomingBranchSeqs.append(incomingSeq)
                    print(f'previous {incomingSeq.getHashList(evtAttr)}')
                    uniqueEvts.extend(
                        incomingSeq.getUniqueValueHashes(evtAttr))

                if len(seq.events) > ind:
                    outgoingSeq = Sequence(
                        seq.events[ind+1:len(seq.events)], seq.eventstore)
                    self.branchSequences[outgoingSeq.getPathID()] = outgoingSeq

                    outgoingSeq.setVolume(seq.getVolume())
                    trailingSeqSegs.append(outgoingSeq)
                    print(f'next {outgoingSeq.getHashList(evtAttr)}')

                indices.extend(range(seq.getVolume()))

                print(f'type {seq.events[ind].type}')

                # REAL TIME STAMPS- NEEDS FIX
                # if seq.events[ind].type == "point":

                #    relTimestamps.append(
                #        seq.events[ind].timestamp-seq.events[0].timestamp)
                # else:
                #    relTimestamps.append(
                #        seq.events[ind].time[0]-seq.events[0].time[0])

        node.setIncomingBranchUniqueEvts(len(set(uniqueEvts)))
        node.setSeqCount(Sequence.getSeqVolume(incomingBranchSeqs))
        node.setPositions(indices)
        node.setRelTimeStamps(relTimestamps)
        node.setIncomingSequences(incomingBranchSeqs)
        print(f'seq count {node.getSeqCount()}')
        print(f'Seq len trailing {len(trailingSeqSegs)}')
        print(f'Seq len not contain {len(notContain)}')

    def run(self, seqs, evtAttr, parent, minval, maxval, checkpoints, excludedEvts, exitNodeHash):
        """Implement CoreFlow algo which takes a list of sequences, a TreeNode (root),
        the attribute to perform mining on, checkpoints from where to start mining,
        list of evenys yo exclude and other CoreFlow parameters.
    """
        if len(checkpoints) > 0:
            containSegs = []
            notContain = []

            node = TreeNode()
            node.attr = evtAttr
            # First integer event
            hashVal = checkpoints[0]
            eVal = seqs[0].getEvtAttrValue(evtAttr, hashVal)
            node.setName(str(eVal))  # NOT sure
            node.setValue(eVal)
            node.setHash(hashVal)
            node.keyevts = parent.keyevts[:]
            node.keyevts.append(hashVal)
            del checkpoints[0]
            self.truncateSequences(
                seqs, hashVal, evtAttr, node, containSegs, notContain)

            parent.children.append(node)

            self.run(containSegs, evtAttr, node, minval, maxval,
                     checkpoints, excludedEvts, exitNodeHash)
            self.run(notContain, evtAttr, parent, minval, maxval,
                     checkpoints, excludedEvts, exitNodeHash)

        else:
            if Sequence.getSeqVolume(seqs) < minval:
                CoreFlowMiner.bundleToExit(seqs, parent, evtAttr, exitNodeHash)
                return

            self.rankingFunc.setEvtAttr(evtAttr)
            # print(f'maxval {maxval}')
            self.rankingFunc.performRanking(seqs, maxval, excludedEvts)
            topPattern = self.rankingFunc.getTopEventSet()
            print(f'topPattern {topPattern.keyEvts}')

            if topPattern is None:
                print("no patterns found")
                CoreFlowMiner.bundleToExit(seqs, parent, evtAttr, exitNodeHash)
                return
            containSegs = []
            notContain = []

            node = TreeNode()
            hashVal = topPattern.getEvents()[0]
            eVal = seqs[0].getEvtAttrValue(evtAttr, hashVal)
            node.setName(str(eVal))  # NOT sure
            node.setValue(eVal)
            node.setHash(hashVal)
            node.attr = evtAttr
            node.keyevts = parent.keyevts[:]
            node.keyevts.append(hashVal)
            print(f'value {eVal}')

            self.truncateSequences(
                seqs, hashVal, evtAttr, node, containSegs, notContain)
            node.setSeqCount(Sequence.getSeqVolume(containSegs))
            print(f'seq count {node.getSeqCount()}')

            if node.getSeqCount() >= minval:
                parent.children.append(node)
                self.run(containSegs, evtAttr, node, minval, maxval,
                         checkpoints, excludedEvts, exitNodeHash)
                self.run(notContain, evtAttr, parent, minval,
                         maxval, checkpoints, excludedEvts, exitNodeHash)

            else:
                CoreFlowMiner.bundleToExit(seqs, parent, evtAttr, exitNodeHash)
                return
