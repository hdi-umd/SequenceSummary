from EventStore import EventStore
from Pattern import Pattern
from CoreFlowMiner import CoreFlowMiner
from Sequence import Sequence


def main():
    sequence_braiding = EventStore.importPointEvents('sequence_braiding_refined.csv', 0, "%m/%d/%y", sep=',', local=True)
    #print(type(sequence_braiding))
    seq=sequence_braiding
    #Sequence.create_attr_dict([seq])
    #seq.getEventPosition('Meal','Lunch')
    #print(seq.getUniqueValueHashes('Meal'))
    #print(seq.getHashList('Glucose'))

    print(seq.getValueHashes('Glucose'))

    #print(seq.getEventsHashString('Glucose'))
    raw_seq=seq.convertToVMSPReadable('Meal')
    print(seq.convertToVMSPReadable('Glucose'))
    #print(seq.getPathID())
    #sequence_braiding[0].attributes.keys()
    #print(sequence_braiding[0].getAttrVal('Meals'))
    #print(sequence_braiding[0].type)
    #for events in sequence_braiding:
    #    print(events.getAttrVal('Meal'))

    seq_list=EventStore.splitSequences(sequence_braiding, "week")
    #seq_list=[]
    #for seqs in sequence_braiding_split:
    #    seq_list.append(Sequence(seqs))
        
    #Sequence.create_attr_dict(seq_list)
    raw_seq="\n".join( seqs.convertToVMSPReadable('Meal') for seqs in seq_list)

    print(raw_seq)


    pat=Pattern([233,309,106,166])
    print(pat.keyEvts)
    #print(pat.filterPaths([seq],'Glucose'))
    #print(pat.getUniqueEventsString())
    print(pat.getPositions([233,309,80,168],seq.getValueHashes('Glucose')))

    ### following code throws an error ###
    # cfm= CoreFlowMiner()
    # root=cfm.getNewRootNode(Sequence.getSeqVolume(seq_list), seq_list)
    # cfm.run(seq_list, "Meal", root, 5 * Sequence.getSeqVolume(seq_list)/100.0, Sequence.getSeqVolume(seq_list), [], {}, -1)
main()