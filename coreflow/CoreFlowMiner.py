import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from helper import get_dataframe, get_time_to_sort_by, insert_event_into_dict
from FrequencyMedianRankingFunction import FrequencyMedianRankingFunction
from OccurrencesMeanRankingFunction import OcccurrencesMeanRankingFunction
from TreeNode import TreeNode
from Sequence import Sequence


class CoreFlowMiner:

    # Implement CoreFlow algo which takes a list of sequences, a TreeNode (root), and a bunch of CoreFlow parameters

    def __init__(self):
        self.branchSequences = {}
        self.rf = FrequencyMedianRankingFunction()

    def checkForStop(self, seqs, minval, checkpoints):
        pass

    def adjustMin(self, seqs, minval):
        if minval < 50:
            return minval

        while(Sequence.getSeqVolume(seqs) < minval and minval > 50):
            minval = minval/2

        return minval

    def bundleToExit(self, seqs, parent, attr, exitNodeHash):
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
            node.setValue(seqs[0].getEvtAttrValue(attr, exitNodeHash))
            node.setHash(exitNodeHash)

        node.setIncomingSequences(seqs, attr)
        node.setSeqCount(Sequence.getSeqVolume(seqs))
        print(f'exit node seq count {node.seqCount}')
        lengths = []
        for s in seqs:
            for i in range(0, s.getVolume()):
                lengths.append(len(s.events)-1)
        node.setPositions(lengths)
        parent.children.append(node)

    # needs properimplementation
    def getNewRootNode(self, numPaths, seqlist, attr):
        print("Start of all " + str(len(seqlist))+" visits")
        return TreeNode("root", numPaths, "-1", attr)

    def truncateSequences(self, seqs, hashval, evtAttr, node, trailingSeqSegs, notContain):
        indices = []
        uniqueEvts = []
        relTimestamps = []
        incomingBranchSeqs = []

        #print(f'hashval {hashval}')
        for seq in seqs:
            i = seq.getEventPosition(evtAttr, hashval)
            #print(f'Position {i}')
            if i < 0:
                notContain.append(seq)
                print(f'not contain {seq.getHashList(evtAttr)}')
            else:
                if i >= 1:
                    incomingSeq = Sequence(seq.events[0:i], seq.eventstore)
                    self.branchSequences[incomingSeq.getPathID()] = incomingSeq
                    incomingSeq.setVolume(seq.getVolume())
                    incomingBranchSeqs.append(incomingSeq)
                    print(f'previous {incomingSeq.getHashList(evtAttr)}')
                    uniqueEvts.extend(
                        incomingSeq.getUniqueValueHashes(evtAttr))

                if len(seq.events) > i:
                    outgoingSeq = Sequence(
                        seq.events[i+1:len(seq.events)], seq.eventstore)
                    self.branchSequences[outgoingSeq.getPathID()] = outgoingSeq

                    outgoingSeq.setVolume(seq.getVolume())
                    trailingSeqSegs.append(outgoingSeq)
                    print(f'next {outgoingSeq.getHashList(evtAttr)}')

                for k in range(0, seq.getVolume()):
                    indices.append(i)
                relTimestamps.append(
                    seq.events[i].timestamp-seq.events[0].timestamp)
        #print(f'Time Stamp {relTimestamps}')
        #print(f'unique {uniqueEvts}')
        #print(f'unique {set(uniqueEvts)}')
        #print(f'unique {len(set(uniqueEvts))}')

        node.setIncomingBranchUniqueEvts(len(set(uniqueEvts)))
        node.setSeqCount(Sequence.getSeqVolume(incomingBranchSeqs))
        node.setPositions(indices)
        node.setRelTimeStamps(relTimestamps)
        node.setIncomingSequences(incomingBranchSeqs, evtAttr)
        print(f'seq count {node.getSeqCount()}')
        #print(f' pos {node.pos}')
        print(f'Seq len trailing {len(trailingSeqSegs)}')
        print(f'Seq len not contain {len(notContain)}')

    def run(self, seqs, evtAttr, parent, minval, maxval, checkpoints, excludedEvts, exitNodeHash):
        if len(checkpoints) > 0:
            containSegs = []
            notContain = []

            node = TreeNode()
            node.attr = evtAttr
            # First integer event
            hashval = checkpoints[0]
            #print(f'hashval {hashval}')
            eVal = seqs[0].getEvtAttrValue(evtAttr, hashval)
            #print(f'eVal {eVal}')
            node.setName(str(eVal))  # NOT sure
            node.setValue(eVal)
            node.setHash(hashval)
            node.keyevts = parent.keyevts[:]

            node.keyevts.append(hashval)
            del checkpoints[0]
            self.truncateSequences(
                seqs, hashval, evtAttr, node, containSegs, notContain)

            parent.children.append(node)

            self.run(containSegs, evtAttr, node, minval, maxval,
                     checkpoints, excludedEvts, exitNodeHash)
            self.run(notContain, evtAttr, parent, minval, maxval,
                     checkpoints, excludedEvts, exitNodeHash)

        else:
            #print(f'minval {minval}')
            #print(f'Seq volume {Sequence.getSeqVolume(seqs)}')
            if Sequence.getSeqVolume(seqs) < minval:
                self.bundleToExit(seqs, parent, evtAttr, exitNodeHash)
                return

            else:
                self.rf.setEvtAttr(evtAttr)
                #print(f'maxval {maxval}')
                self.rf.performRanking(seqs, maxval, excludedEvts)
                topPattern = self.rf.getTopEventSet()
                print(f'topPattern {topPattern.keyEvts}')

                if topPattern is None:
                    print("no patterns found")
                    self.bundleToExit(seqs, parent, evtAttr, exitNodeHash)
                    return
                containSegs = []
                notContain = []

                node = TreeNode()
                hashval = topPattern.getEvents()[0]
                eVal = seqs[0].getEvtAttrValue(evtAttr, hashval)
                node.setName(str(eVal))  # NOT sure
                node.setValue(eVal)
                node.setHash(hashval)
                node.attr = evtAttr
                node.keyevts = parent.keyevts[:]
                node.keyevts.append(hashval)
                print(f'value {eVal}')

                self.truncateSequences(
                    seqs, hashval, evtAttr, node, containSegs, notContain)
                node.setSeqCount(Sequence.getSeqVolume(containSegs))
                print(f'seq count {node.getSeqCount()}')

                if node.getSeqCount() >= minval:
                    parent.children.append(node)
                    self.run(containSegs, evtAttr, node, minval, maxval,
                             checkpoints, excludedEvts, exitNodeHash)
                    self.run(notContain, evtAttr, parent, minval,
                             maxval, checkpoints, excludedEvts, exitNodeHash)

                else:
                    self.bundleToExit(seqs, parent, evtAttr, exitNodeHash)
                    return
