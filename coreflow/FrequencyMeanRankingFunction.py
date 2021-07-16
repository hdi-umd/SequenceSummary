import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Pattern import Pattern

class FrequencyMeanRankingFunction:
    def __init__(self):
        self.topRankedEvtValues=[]
        self.evtAttr=""
        
    def setEvtAttr(self, evtAttr):
        self.evtAttr=evtAttr
        #print(f'evtattr {self.evtAttr}')

    def getTopEventSet(self):
        if not self.topRankedEvtValues:
            return None
        elif len(self.topRankedEvtValues)==1:
            return self.topRankedEvtValues[0]
        else:
            #for k in self.topRankedEvtValues:
            #    print(f'top key {k.keyEvts}')

            for p in self.topRankedEvtValues:
                p.computePatternStats(self.evtAttr)
            
            #for k in self.topRankedEvtValues:
            #    print(f'sorted key {k.keyEvts}')

            self.topRankedEvtValues=sorted(self.topRankedEvtValues, key=lambda x: x.getEventMeanPos()[0])
        
        return self.topRankedEvtValues[0]
    
    def performRanking(self, seqs, maxSup, excludedEvts):
        result={}
        
        evtValueKey=""
        uniqueHashes=[]
        
        for seq in seqs:
            # get hashlist for each individual sequence
            uniqueHashes= seq.getUniqueValueHashes(self.evtAttr)
            #print(f'evthash {evtHashes}')
            for hashval in uniqueHashes:
                
                if hashval in excludedEvts:
                    continue
                evtValueKey=str(hashval)
                
                #create a pattern for all hash values
                if evtValueKey  not in result.keys():
                    #print(f'evtValueKey {evtValueKey}')
                    p=Pattern([evtValueKey])
                    #p.addKeyEvent(hashval)
                    result[evtValueKey]=p
                    
                result[evtValueKey].addToSupportSet(seq)
        #print(result.keys())
        #print(result.values())
        
        
        s=[]
        #print(f'maxSup {maxSup}')
        
        for itr in result.values():
            #print(itr.keyEvts)
            if(itr.getSupport()>maxSup):
                continue
            s.append(itr)
        
        if not s:
            return
        
        #for patterns in s:
            #print(f'pat before sort {patterns.keyEvts}')
        s=sorted(s, key= lambda x: x.getSupport(), reverse=True)
        
        self.topRankedEvtValues=[]
        
        maxval= s[0].getSupport()
        #print(f'maxval {maxval}')
        
        for patterns in s:
            #print(f'pat {patterns.keyEvts}')
            #print(f'support {patterns.getSupport()}')
            if patterns.getSupport() < maxval:
                break
            self.topRankedEvtValues.append(patterns)
        #print(len(s))
        #print(len(self.topRankedEvtValues))
        #for k in self.topRankedEvtValues:
        #    print(f'key {k.keyEvts}')

        #print(f'top ranked {*(k.keyEvts for k in self.topRankedEvtValues)}')
