from .Sequence import Sequence
from .TreeNode import TreeNode
from .OccurrencesMeanRankingFunction import OccurrencesMeanRankingFunction

class CoreFlowMiner:
    rf=OccurrencesMeanRankingFunction()
    # Implement CoreFlow algo which takes a list of sequences, a TreeNode (root), and a bunch of CoreFlow parameters 

    def __init__(self):
        self.branchSequences={}
        
    
    def checkForStop(seqs, minval, checkpoints):
        pass
    
    def adjustMin(seqs, minval):
        if minval<50 :
            return minval
        
        while(Sequence.getSeqVolume(seqs)<minval and minval>50):
            minval=minval/2
        
        return minval
    
    def bundleToExit(self, seqs, parent, attr, exitNodeHash):
        if len(seqs)==0:
            return
        
        node=TreeNode()
        
        if exitNodeHash==-1:
            node.setName("Exit")
            node.setValue("Exit")
            node.setHash(-1)
            
        else:
            node.setName(str(Sequence.getEvtAttrValue(attr,exitNodeHash)))
            node.setValue(Sequence.getEvtAttrValue(attr,exitNodeHash))
            node.setHash(exitNodeHash)
        
        node.setIncomingSequences(seqs, attr)
        node.setSeqCount(Sequence.getSeqVolume(seqs))
        
        lengths=[]
        for s in seqs:
            for i in range(0,s.getVolume()):
                lengths.append(len(s.events)-1)
        node.setPositions(lengths)
        parent.append(node)
        
    #needs properimplementation    
    def getNewRootNode(self, numPaths, seqlist):
        return TreeNode("Start of all "+ str(len(seqlist))+" visits", numPaths, "-1")
    
    
    def truncateSequences(self, seqs, hashval, evtAttr, node,trailingSeqSegs, notContain):
        indices=[]
        uniqueEvts=[]
        relTimestamps=[]
        incomingBranchSeqs=[]
        
        for seq in seqs:
            i=seq.getEventPosition(evtAttr, hashval)
            print(i)
            if i is None:
                notContain.append(seq)
            else:
                if i>1:
                    incomingSeq= Sequence(seq.events[0:i])
                    self.branchSequences[incomingSeq.getPathID()]= incomingSeq
                    incomingSeq.setVolume(seq.getVolume())
                    incomingBranchSeqs.append(incomingSeq)
                    
                    uniqueEvts.extend(incomingSeq.getUniqueValueHashes(evtAttr))
                    
                if len(seq.events)>i+2:
                    outgoingSeq= Sequence(seq.events[i+1:len(seq.events)])
                    self.branchSequences[outgoingSeq.getPathID()]= outgoingSeq
                    
                    outgoingSeq.setVolume(seq.getVolume())
                    trailingSeqSegs.append(outgoingSeq)
                    
                for k in range(0, seq.getVolume()):
                    indices.append(i)
                relTimestamps.append(seq.events[i].timestamp-seq.events[0].timestamp)
        print(f'Time Stamp {relTimestamps}')
        print(f'unique {uniqueEvts}')
        print(f'unique {set(uniqueEvts)}')
        print(f'unique {len(set(uniqueEvts))}')
                
        node.setIncomingBranchUniqueEvts( len(set(uniqueEvts)) )
        node.setSeqCount(Sequence.getSeqVolume(incomingBranchSeqs))
        node.setPositions(indices)
        node.setRelTimeStamps(relTimestamps)
        node.setIncomingSequences(incomingBranchSeqs, evtAttr)

            
    def run(self, seqs, evtAttr, parent, minval, maxval, checkpoints, excludedEvts, exitNodeHash ):
        if len(checkpoints)>0:
            containSegs=[]
            notContain=[]
            
            node= TreeNode()
            
            #First integer event
            hashval=checkpoints[0]
            eVal=Sequence.getEvtAttrValue(evtAttr, hashval)
            node.setName(str(eVal)) #NOT sure
            node.setValue(eVal)
            node.setHash(hashval)
            del checkpoints[0]
            self.truncateSequences(seqs, hashval, evtAttr, node, containSegs, notContain)
            
            parent.append(node)
            
            self.run(containSegs, evtAttr, [node], minval, maxval, checkpoints, excludedEvts, exitNodeHash)
            self.run(notContain, evtAttr, [parent], minval, maxval, checkpoints, excludedEvts, exitNodeHash)
            
        else:
            print(f'minval {minval}')
            print(f'Seq volume {Sequence.getSeqVolume(seqs)}')
            if Sequence.getSeqVolume(seqs)<minval:
                self.bundleToExit(seqs, parent, evtAttr, exitNodeHash)
                return 
            
            else:
                self.rf.setEvtAttr(evtAttr)
                print(f'maxval {maxval}')
                self.rf.performRanking(seqs, maxval, excludedEvts)
                topPattern=self.rf.getTopEventSet()
                
                if topPattern is None:
                    print("no patterns found")
                    self.bundleToExit(seqs, parent, evtAttr, exitNodeHash)
                
                containSegs=[]
                notContain=[]
                
                node= TreeNode()
                hashval=topPattern.getEvents()[0]
                eVal=Sequence.getEvtAttrValue(evtAttr, hashval)
                node.setName(str(eVal)) #NOT sure
                node.setValue(eVal)
                node.setHash(hashval)

                self.truncateSequences(seqs, hashval, evtAttr, node, containSegs, notContain)
                node.setSeqCount(Sequence.getSeqVolume(containSegs))
                
                if node.getSeqCount()>minval:
                    parent.append(node)
                    self.run(containSegs, evtAttr, [node], minval, maxval, checkpoints, excludedEvts, exitNodeHash)
                    self.run(notContain, evtAttr, [node], minval, maxval, checkpoints, excludedEvts, exitNodeHash)
                
                else:
                    self.bundleToExit(seqs, parent, evtAttr, exitNodeHash)
                    return