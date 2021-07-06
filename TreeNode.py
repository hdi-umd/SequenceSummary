from itertools import count
import numpy as np
import json
from datetime import datetime, timedelta

class Node():
    NID=count(1)
    nodeHash={}
    
    
    def __init__(self, name="", count=0, value="", attr=""):
        super().__init__()
        self.nid=next(self.NID)
        self.name=name
        self.seqCount=count
        ## What's the difference between name and value?
        self.value=value
        self.hash=-1
        self.pos=[]
        self.meanStep=0
        self.medianStep=0
        #self.zipCompressRatio=0
        self.incomingBranchUniqueEvts=None
        #self.incomingBranchSimMean=None
        #self.incomingBranchSimMedian=None
        #self.incomingBranchSimVariance=None
        self.keyevts=[]
        
        self.incomingSequences=[]
        self.outgoingSequences=[]
        
        self.meanRelTimestamp=0
        self.medianRelTimestamp=0
        

        self.attr=attr

        TreeNode.nodeHash[self.nid]=self
        
        
    def getNode(self, node_id):
        return nodeHash[node_id]
    
    def clearHash(self):
        nodeHash.clear()
        
    def getIncomingSequences(self):
        return self.incomingSequences
    
    def getSeqCount(self):
        return self.seqCount
    
    def setSeqCount(self, seqCount):
        self.seqCount=seqCount
        
    def getName(self):
        return self.name
    
    def setName(self, name):
        self.name=name
        
    def getMeanStep(self):
        return self.meanStep
    
    #need a better implementation
    def toJSONObject(self):
        return json.dumps(self, default=lambda o: o.__dict__)#,sort_keys=True, indent=4) 
    
    def toString(self):
        return self.name+": "+self.seqCount
    
    def setPositions(self, l):
        self.pos=l
        self.pos.sort()
        d=sum(self.pos)+len(self.pos)
        mid=len(self.pos)/2
        
        if len(self.pos)==0:
            self.meanStep=0
            self.medianStep=0
        else:
            #WHY WE ARE ADDING 1 to mean and medianStep?
            self.meanStep=d/(len(self.pos))-1
            self.medianStep= np.median(self.pos)+1#((self.pos[mid-1]+self.pos[mid])/2.0)+1 if len(self.pos)%2==0 else self.pos[mid]+1
            
    def getValue(self):
        return self.value
    
    def setValue(self, value):
        self.value=value
        
    def getMedianStep(self):
        return self.medianStep
    
    #def getZipCompressRatio(self):
    #    return self.zipCompressRatio
    
    #def setZipCompressRatio(self, zipcompressratio):
    #    self.zipCompressRatio=zipcompressratio
        
    def getIncomingBranchUniqueEvts(self):
        return self.incomingBranchUniqueEvts
    
    def setIncomingBranchUniqueEvts(self, incomingbranchuniqueevts):
        self.incomingBranchUniqueEvts=incomingbranchuniqueevts
        
    #def setIncomingBranchSimilarityStats(self, mean, median, variance):
    #    self.incomingBranchSimMean=mean
    #    self.incomingBranchSimMedian=median
    #    self.incomingBranchSimVariance=variance
        
    
    def setIncomingSequences(self, incomingbrancseqs, evtattr):
        self.incomingSequences=incomingbrancseqs
        
    def setRelTimeStamps(self, reltimestamps):
        #print(f'Time Stamp {reltimestamps}')
        #print(f'Time Stamp {type(reltimestamps[0])}')
        reltimestamps.sort()
        #print(f'Time Stamp {reltimestamps}')
        #print(f'Time Stamp {type(reltimestamps[0])}')
        
        d=sum(reltimestamps, timedelta())
        
        mid=len(reltimestamps)/2
        
        if(len(reltimestamps)==0):
            self.meanRelTimestamp=0
            self.medianRelTimestamp=0
            
        else:
        
            self.meanRelTimestamp=d*1.0/len(reltimestamps)
            self.medianRelTimestamp=np.median(reltimestamps) #(reltimestamps[mid-1]+reltimestamps[mid])/2.0 if len(reltimestamps%2==0) else reltimestamps[mid]
        
        #print(f'Time Stamp {self.meanRelTimestamp}')
        #print(f'Time Stamp {self.meanRelTimestamp}')

    def getPatternString(self):
        return "-".join(str(self.incomingSequences[0].eventstore.reverseatttrdict[self.attr][hashval]) for hashval in self.keyevts if self.incomingSequences)

    def getHash(self):
        
        return self.hash
        
    def setHash(self, value):
        self.hash=value
        
        
        
    #def json_serialize(self):
    #    json.dump(self, indent=4, default= TreeNode.json_default_dump)

    def json_default_dump(self)-> dict:
        pass
    
    def json_serialize(self) -> None:
    
        pass
    
    @staticmethod
    def json_serialize_dump(obj):
    
        pass

class TreeNode(Node):
    def __init__(self, name="", count=0, value="", attr=""):
        super().__init__(name, count, value)
        self.children = []

    def json_default_dump(self)-> dict:
        return {
            "event_attribute": self.value,
            "Pattern": self.getPatternString(),
            "value": self.seqCount,
            "median_index": self.medianStep,
            "average_index":self.meanStep,

            "children":[TreeNode.json_serialize_dump(x) for x in self.children]
            
        }
    
    def json_serialize(self) -> None:
    
        json.dump(self,  indent=4, default=TreeNode.json_serialize_dump)
    
    @staticmethod
    def json_serialize_dump(obj):
    
        if hasattr(obj, "json_default_dump"):
            
            return obj.json_default_dump()
        return None



class GraphNode(Node):
    def __init__(self, name="", count=0, value="", attr=""):
        super().__init__(name, count, value, attr)
        self.before = []
        self.after = []
        
    def json_default_dump(self)-> dict:
        return {
            "before": GraphNode.json_serialize_dump(self.before),
            "event_attribute": self.value,
            "Pattern": self.getPatternString(),
            "value": self.seqCount,
            "After": GraphNode.json_serialize_dump(self.after)

        }

    def json_serialize(self) -> None:
    
        json.dump(self,  indent=4, default=GraphNode.json_serialize_dump)
    
    @staticmethod
    def json_serialize_dump(obj):
    
        if hasattr(obj, "json_default_dump"):
            
            return obj.json_default_dump()
        return None

    

    