#collection of events sharing similar property 

from itertools import count
class Sequence:
    _ids = count(0)
    
    attrdict={}
    reverseatttrdict={}
    def __init__(self, events, sid=None):
        # sequence id
        if sid is None:
            self.sid = next(self._ids)
        else:
            self.sid = sid
        
        self.events = events
        self.volume=1
        self.seqAttributes={}
    def getEventPosition(self, attr, hash_val):
        for count,event in enumerate(self.events):
            #if event.getAttrVal(attr)==hash_val:
            if Sequence.attrdict[attr][event.getAttrVal(attr)]==hash_val:
                return count
        return -1
    
    def setVolume(self, intValue):
        self.volume=intValue
        
    def getVolume(self):
        return self.volume
    
    def increaseVolume(self):
        self.volume += 1 
    
    
    def getUniqueValues(self, attr):
        l=list(set(event.getAttrVal(attr) for event in self.events))
        return l
    
    def getUniqueValueHashes(self, attr):
        l=list(set(event.getAttrVal(attr) for event in self.events))
        uniquelist=[Sequence.attrdict[attr][elem] for elem in l]
        return uniquelist
    
    #Not sure this will always result in same index, will change if 
    #dictionary is updated
    #since python is unordered
    
    def getHashList(self, attr):
        #l=list(list(event.attributes.keys()).index(attr) for event in self.events)
        l=[event.getAttrVal(attr) for event in self.events]
        hashlist=[Sequence.attrdict[attr][elem] for elem in l]
        
        return hashlist
    
    def getValueHashes(self, attr):
        l=list(event.getAttrVal(attr) for event in self.events)
        hashlist=[Sequence.attrdict[attr][elem] for elem in l]
        
        return hashlist
        
    
    def getEventsHashString(self, attr):
        s=attr+": "
        l=list(event.getAttrVal(attr) for event in self.events)
        #for count,event in enumerate(self.events):
        #    s+=str(event.getAttrVal(attr))+" "
        s+="".join(str(Sequence.attrdict[attr][elem]) for elem in l)
        return s
    
    def convertToVMSPReadablenum(self, attr):
        l=list(event.getAttrVal(attr) for event in self.events)
        s=" -1 ".join(str(Sequence.attrdict[attr][elem]) for elem in l)
        #s=""
        #for count,event in enumerate(self.events):
        #    s+=str(event.getAttrVal(attr))+" -1 "
        s+=" -2"
        
        return s
    
    def convertToVMSPReadable(self, attr):
        l=list(event.getAttrVal(attr) for event in self.events)
        s=" ".join(Sequence.attrdict[attr][elem] for elem in l)
        #s=""
        #for count,event in enumerate(self.events):
        #    s+=str(event.getAttrVal(attr))+" -1 "
        s+="."
        
        return s
    
    def getPathID(self):
        return self.sid
    
    def matchPathAttribute(self, attr):
        # should i use eq?!
        if this.seqAttributes.get(attr)==(val):
            return True
        else:
            return False
        
    def setSequenceAttribute(self,attr, value):
        self.seqAttributes[attr]=value
        
         

    # equivalent to method signature public static int getVolume(List<Sequence> seqs)    
    def getSeqVolume(seqlist):
        return sum(seq.getVolume() for seq in seqlist)
    
    
    # Method equivalent to public String getEvtAttrValue(String attr, int hash) in DataManager.java
    def getEvtAttrValue(attr, hashval):
        return Sequence.reverseatttrdict[attr][hashval]
        
    # Method equivalent to public List<String> getEvtAttrValues(String attr) in DataManager.java    
    def getEvtAttrValues(attr):
        return list(Sequence.reverseatttrdict[attr].values())
    
    # Method equivalent to int getEvtAttrValueCount(String attr) in DataManager.java    
    def getEvtAttrValueCount(attr):
        return len(Sequence.reverseatttrdict[attr])