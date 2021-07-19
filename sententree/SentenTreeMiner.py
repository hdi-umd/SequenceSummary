import numpy as np
from Graph import Rawnode, Links
from TreeNode import GraphNode
from Sequence import Sequence


class SentenTreeMiner:

    def __init__(self):

        self.rf = self.first_occurrence
        self.tb = self.performRanking_medianIndex

    def expandSeqTree(self, attr, rootNode,  expandCnt, minSupport, maxSupport, graph):

        # if len(rootSeq.eventlist>0):
        expandCnt -= len(rootNode.keyevts)

        seqs = []
        seqs.append(rootNode)
        rootNode.setSeqCount(Sequence.getSeqVolume(rootNode.incomingSequences))
        rootNode.attr = attr
        leafSeqs = []

        graph.nodes.append(Rawnode(rootNode))
        while seqs and expandCnt > 0:
            s = max(seqs, key=lambda x: x.seqCount)
            print(f'seqCount: {s.seqCount}')
            #print(f'this: {s}')

            s0 = s.after
            s1 = s.before

            #print(f' s : {s}')
            #print(f' s0 : {s0}')
            #print(f' s1: {s1}')

            print(f'this.pattern s : {s.keyevts}')
            #print(f'this.pattern s0 : {s0.keyevts}')
            #print(f'this.pattern s1: {s1.keyevts}')

            if not s1 and not s0:
                word, pos, count, s0, s1 = self.growSeq(
                    attr, s,  minSupport, maxSupport)
                print(f'word: {word}, pos: {pos}, count: {count}')

                if count < minSupport:
                    leafSeqs.append(s)
                else:

                    s1.setHash(word)
                    s1.setValue(
                        s.incomingSequences[0].getEvtAttrValue(attr, word))
                    s1.keyevts = s.keyevts[:]  # deep copy
                    s0.keyevts = s.keyevts[:]
                    # for i,x in enumerate(s.pattern.keyEvts):
                    #    print(s.pattern.keyEvts)
                    #    s1.pattern.addKeyEvent(x)
                    #    s0.pattern.addKeyEvent(x)

                    s1.keyevts.insert(pos, word)

                #print(f'this.pattern s after: {s.keyevts}')
                #print(f'this.pattern s0 after: {s0.keyevts}')
                #print(f'this.pattern s1 after: {s1.keyevts}')

            if s1 and s1.seqCount >= minSupport:
                expandCnt -= 1
                seqs.append(s1)
                graph.nodes.append(Rawnode(s1))
                graph.links.append(Links(s.nid, s1.nid, s1.seqCount))

                # s1.after=s
            s.before = s1
            s.after = s0

            if s0 and s0.seqCount >= minSupport:
                seqs.append(s0)
                # graph.nodes.append(Rawnode(s0))

                # graph.add(s.nid,s0.nid)

                # s0.before=s
            print(f'seqCount: {[s.seqCount for s in seqs]}')
            #print(f'before: {s.before}')
            #print(f'after: {s.after}')
            #print(f'this: {s}')
            #print(f' s after: {s}')
            #print(f' s0 after: {s0}')
            #print(f' s1 after: {s1}')

            del seqs[seqs.index(s)]
            #print(f'seqCount: {[s.seqCount for s in seqs]}')
            #print(f'before: {seqs[0].before}')
            #print(f'after: {seqs[0].after}')
            #print(f'this: {seqs[0]}')

            #print(f' s : {s}')
            #print(f' s0 : {s0}')
            #print(f' s1: {s1}')

        return leafSeqs.append(seqs)

    def performRanking_naive(self, fdist, _fdist_ind, i, _pos, count, maxSupport, _minpos):
        maxw = ""
        maxc = 0
        for w in fdist.keys():
            value = fdist[w]

            if value < maxSupport and value > maxc:
                maxw = str(w)
                maxc = value

        if maxc > count:
            return i, maxw, maxc, True

        return i, maxw, maxc, False

    def performRanking_meanIndex(self, fdist, fdist_ind, i, pos, count, maxSupport, minpos):
        maxw = ""
        maxc = 0

        for w in fdist.keys():
            value = fdist[w]

            mean_pos = sum(fdist_ind[w]) / len(fdist_ind[w])

            if value <= maxSupport and value > maxc:
                maxw = str(w)
                maxc = value
                minpos = mean_pos

            if value == maxc and mean_pos < minpos:
                maxw = str(w)
                maxc = value
                minpos = mean_pos

        if maxc > count or (maxc == count and pos < i):
            return i, maxw, maxc, True

        return i, maxw, maxc, False

    def performRanking_medianIndex(self, fdist, fdist_ind, i, pos,  count, maxSupport, minpos):
        maxw = ""
        maxc = 0

        for w in fdist.keys():
            value = fdist[w]

            meadin_pos = np.median(fdist_ind[w])

            if value <= maxSupport and value > maxc:
                maxw = str(w)
                maxc = value
                minpos = meadin_pos

            if value == maxc and meadin_pos < minpos:
                maxw = str(w)
                maxc = value
                minpos = meadin_pos

        if maxc > count or (maxc == count and pos < i):
            return i, maxw, maxc, True

        return i, maxw, maxc, False

    def first_occurrence(self, fdist, evtHashes, l, r, s, fdist_ind=None):

        if fdist_ind is None:
            fdist_ind = {}
        duplicate = []
        for j in range(l, r):
            w = evtHashes[j]
            # print(w)
            if w in duplicate:
                continue
            duplicate.append(w)
            if w not in fdist:
                fdist[w] = s.getVolume()
                fdist_ind[w] = [j]
            else:
                fdist[w] += s.getVolume()
                fdist_ind[w].append(j)

    def all_occurrence(self, fdist, evtHashes, l, r, s, fdist_ind=None):

        if fdist_ind is None:
            fdist_ind = {}

        for j in range(l, r):
            w = evtHashes[j]
            # print(w)
            if w not in fdist:
                fdist[w] = s.getVolume()
                fdist_ind[w] = [j]
            else:
                fdist[w] += s.getVolume()
                fdist_ind[w].append(j)

    def growSeq(self, attr, seq,  minSupport, maxSupport):

        pos = -1
        word = ""
        count = 0

        for i in range(0, len(seq.keyevts)+1):
            fdist = {}
            fdist_ind = {}

            for s in seq.incomingSequences:

                evtHashes = s.getHashList(attr)
                l = 0 if i == 0 else s.seqIndices[i - 1] + 1
                r = len(evtHashes) if i == len(
                    seq.keyevts) else s.seqIndices[i]

                self.rf(fdist, evtHashes, l, r, s, fdist_ind)

            minpos = max(len(x.events) for x in seq.incomingSequences)

        
            pos_, word_, count_, verdict = self.tb(
                fdist, fdist_ind, i, pos, count, maxSupport, minpos)
            
            if verdict == True:
                pos = pos_
                word = word_
                count = count_


        s0 = GraphNode(attr=attr)
        s1 = GraphNode(attr=attr)

        #print(f'this.pattern s0 in growseq: {s0.pattern}')
        #print(f'this.pattern s1 in growseq: {s1.pattern}')

        #print(f'minSupport {minSupport} count {count}')
        if count >= minSupport:
            words = seq.keyevts
            for t in seq.incomingSequences:
                l = 0 if pos == 0 else t.seqIndices[pos - 1] + 1
                r = len(t.events) if pos == len(words) else t.seqIndices[pos]
                try:
                    i = t.getHashList(attr).index(word, l, r)
                    #print(f'position: {i}')
                    # i+=l

                    # sequence index value for the word being inserted. e.g. A-C-G seq indice 1,4,8
                    t.seqIndices.insert(pos, i)
                    s1.incomingSequences.append(t)
                    s1.seqCount += t.getVolume()

                except ValueError:
                    #print(f'Value error')
                    s0.incomingSequences.append(t)
                    s0.seqCount += t.getVolume()
            # calculate average index
            pos_arr = [seq.seqIndices[pos] for seq in s1.incomingSequences]
            #print(f'pos_arr {pos_arr}')
            s1.setPositions(pos_arr)
            #print(f'Mean {s1.getMeanStep()} Median {s1.getMedianStep()}')
            s0.setSeqCount(Sequence.getSeqVolume(s0.incomingSequences))
            s1.setSeqCount(Sequence.getSeqVolume(s1.incomingSequences))

            print(f'Not contain: {len(s0.incomingSequences)}')
            print(f'contain: {len(s1.incomingSequences)}')
        return word, pos, count, s0, s1
