import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Sequence import Sequence
from TreeNode import TreeNode, GraphNode



class SentenTreeMiner:
    
    def expandSeqTree(self, attr, rootNode,  expandCnt, minSupport, maxSupport):
        
        #if len(rootSeq.eventlist>0):
        expandCnt-=len(rootNode.keyevts)
        
        seqs = []
        seqs.append(rootNode)
        rootNode.setSeqCount(Sequence.getSeqVolume(rootNode.incomingSequences))
        leafSeqs = []
        
        
        while seqs and expandCnt > 0:
            s = max(seqs,key=lambda x: x.seqCount) 
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
                word, pos, count, s0, s1= self.growSeq(attr, s,  minSupport, maxSupport)
                print(f'word: {word}, pos: {pos}, count: {count}')
                
                
                if count < minSupport:
                    leafSeqs.append(s)
                else:
                    
                    s1.setHash(word)
                    s1.setValue(s.incomingSequences[0].getEvtAttrValue(attr, word))
                    s1.keyevts=s.keyevts[:] #deep copy
                    s0.keyevts=s.keyevts[:]
                    #for i,x in enumerate(s.pattern.keyEvts):
                    #    print(s.pattern.keyEvts)
                    #    s1.pattern.addKeyEvent(x)
                    #    s0.pattern.addKeyEvent(x)
                        
                    s1.keyevts.append(word) 
                
                #print(f'this.pattern s after: {s.keyevts}')
                #print(f'this.pattern s0 after: {s0.keyevts}')
                #print(f'this.pattern s1 after: {s1.keyevts}')
        
                    
            if s1:
                expandCnt-=1
                seqs.append(s1)
            s.before=s1
            s.after=s0
            
            if s0 and s0.seqCount>= minSupport:
                seqs.append(s0)
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
    
    
    def growSeq(self, attr, seq,  minSupport, maxSupport) :
        #this is not right
        pos=-1
        word=""
        count=0
        #print(f'this.pattern in growseq: {seq.pattern}')
        #eventcol=Sequence.getUniqueEvents(seq.incomingSequences)
        #print(f'seq pattern len {seq.keyevts}')
        for i in range (0,len(seq.keyevts)+1):
            fdist={}
            #print(f'i: {i}, len {len(seq.keyevts)}')
            for  ind, s in enumerate(seq.incomingSequences):
                #print(f's.seqIndices: {s.seqIndices}')
                evtHashes= s.getHashList(attr)
                l=0 if i==0 else   s.seqIndices[i - 1] + 1
                r=len(evtHashes) if i==len(seq.keyevts) else s.seqIndices[i]
                
                
                #print(f'l index: {l}, r index {r}')
                print(f'evt Hash: {evtHashes}')
                for j in range (l,r):
                    w=evtHashes[j]
                    #print(w)
                    if w not in fdist:
                        fdist[w] = s.getVolume()
                    else:
                        fdist[w]+= s.getVolume()
                
                maxw=""
                maxc=0
                for w in fdist.keys():
                    value= fdist[w]
                    
                    if value < maxSupport and value > maxc:
                        maxw= str(w)
                        maxc= value
                
                if maxc > count:
                    pos=i
                    word=maxw
                    count=maxc
        #print(f'{word}: word')
        #print(f'{maxc}: count')
                    
        s0=GraphNode()
        s1=GraphNode()
        
        #print(f'this.pattern s0 in growseq: {s0.pattern}')
        #print(f'this.pattern s1 in growseq: {s1.pattern}')
        
        #print(f'minSupport {minSupport} count {count}')    
        if count >= minSupport:
            words=seq.keyevts
            for t in seq.incomingSequences:
                l=0 if pos==0 else t.seqIndices[pos - 1] + 1
                r= len(t.events) if pos == len(words) else  t.seqIndices[pos]
                try:
                    i = t.getHashList(attr).index(word,l,r)
                    #print(f'position: {i}')
                    #i+=l
                    
                    t.seqIndices.insert(pos,i)
                    s1.incomingSequences.append(t)
                    s1.seqCount+=t.getVolume()

                except ValueError:
                    #print(f'Value error')
                    s0.incomingSequences.append(t)
                    s0.seqCount+=t.getVolume()
                
        s0.setSeqCount(Sequence.getSeqVolume(s0.incomingSequences))
        s1.setSeqCount(Sequence.getSeqVolume(s1.incomingSequences))
        print(f'Not contain: {len(s0.incomingSequences)}')
        print(f'contain: {len(s1.incomingSequences)}')
        return word, pos, count, s0, s1    