#collection of events sharing similar property 

from itertools import count
from Event import Event
class Sequence():
    _ids = count(0)
    

    def __init__(self,  eventlist, eventstore,sid=None):
        # sequence id
        if sid is None:
            self.sid = next(self._ids)
        else:
            self.sid = sid
        
        self.events = eventlist
        self.eventstore=eventstore
        self.volume=1
        self.seqAttributes={}
    def getEventPosition(self, attr, hash_val):
        for count,event in enumerate(self.events):
            #if event.getAttrVal(attr)==hash_val:
            if self.eventstore.attrdict[attr][event.getAttrVal(attr)]==hash_val:
                return count
        return -1
    
    def setVolume(self, intValue):
        self.volume=intValue
        
    def getVolume(self):
        return self.volume
    
    def increaseVolume(self):
        self.volume += 1 
    
    
    def getUniqueValueHashes(self, attr):
        l=list(set(event.getAttrVal(attr) for event in self.events))
        uniquelist=[self.eventstore.attrdict[attr][elem] for elem in l]
        return uniquelist
    
    #Not sure this will always result in same index, will change if 
    #dictionary is updated
    #since python is unordered
    
    def getHashList(self, attr):
        #l=list(list(event.attributes.keys()).index(attr) for event in self.events)
        l=[event.getAttrVal(attr) for event in self.events]
        hashlist=[self.eventstore.attrdict[attr][elem] for elem in l]
        
        return hashlist
    
    def getValueHashes(self, attr):
        l=list(event.getAttrVal(attr) for event in self.events)
        hashlist=[self.eventstore.attrdict[attr][elem] for elem in l]
        
        return hashlist
        
    
    def getEventsHashString(self, attr):
        s=attr+": "
        l=list(event.getAttrVal(attr) for event in self.events)
        #for count,event in enumerate(self.events):
        #    s+=str(event.getAttrVal(attr))+" "
        s+="".join(str(self.eventstore.attrdict[attr][elem]) for elem in l)
        return s
    
    def convertToVMSPReadablenum(self, attr):
        l=list(event.getAttrVal(attr) for event in self.events)
        s=" -1 ".join(str(self.eventstore.attrdict[attr][elem]) for elem in l)
        #s=""
        #for count,event in enumerate(self.events):
        #    s+=str(event.getAttrVal(attr))+" -1 "
        s+=" -2"
        
        return s
    
    def convertToVMSPReadable(self, attr):
        l=list(event.getAttrVal(attr) for event in self.events)
        s=" ".join(self.eventstore.attrdict[attr][elem] for elem in l)
        #s=""
        #for count,event in enumerate(self.events):
        #    s+=str(event.getAttrVal(attr))+" -1 "
        s+="."
        
        return s
    
    def getPathID(self):
        return self.sid
    
    def matchPathAttribute(self, attr, val):
        # should i use eq?!
        if self.seqAttributes.get(attr)==(val):
            return True
        else:
            return False
        
    def setSequenceAttribute(self,attr, value):
        self.seqAttributes[attr]=value
        
         

    # equivalent to method signature public static int getVolume(List<Sequence> seqs)    
    def getSeqVolume( seqlist):
        return sum(seq.getVolume() for seq in seqlist)
    
    
    # Method equivalent to public String getEvtAttrValue(String attr, int hash) in DataManager.java
    def getEvtAttrValue(self, attr, hashval):
        return self.eventstore.reverseatttrdict[attr][hashval]
        
    # Method equivalent to public List<String> getEvtAttrValues(String attr) in DataManager.java    
    def getEvtAttrValues(self, attr):
        return list(self.eventstore.reverseatttrdict[attr].values())
    
    # Method equivalent to int getEvtAttrValueCount(String attr) in DataManager.java    
    def getEvtAttrValueCount(self, attr):
        return len(self.eventstore.reverseatttrdict[attr])
    
    