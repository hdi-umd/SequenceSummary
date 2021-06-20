import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from EventStore import EventStore
from Pattern import Pattern
from CoreFlowMiner import CoreFlowMiner
from Sequence import Sequence
from TreeNode import TreeNode
from spmf import Spmf
import pandas as pd
from IPython.display import display
import json
import argparse




def main():
    sequence_braiding_Es= EventStore()
    sequence_braiding_Es.importPointEvents('sequence_braiding_refined.csv', 0, "%m/%d/%y", sep=',', local=True)

    #print(type(sequence_braiding))
    seq=Sequence(sequence_braiding_Es.events, sequence_braiding_Es)

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

    seq_list=Sequence.splitSequences(seq, "week")
    #seq_list=[]
    #for seqs in sequence_braiding_split:
    #    seq_list.append(Sequence(seqs))
        
    #Sequence.create_attr_dict(seq_list)
    raw_seq="\n".join( seqs.convertToVMSPReadable('Meal') for seqs in seq_list)
    #seq_list=[]
    #for seqs in sequence_braiding_split:
    #    seq_list.append(Sequence(seqs))
        
    #Sequence.create_attr_dict(seq_list)
    #raw_seq="\n".join( seqs.convertToVMSPReadable('Meal') for seqs in seq_list)

    print(raw_seq)


    #pat=Pattern([233,309,106,166])
    #print(pat.keyEvts)
    #print(pat.filterPaths([seq],'Glucose'))
    #print(pat.getUniqueEventsString())
    #print(pat.getPositions([233,309,80,168],seq.getValueHashes('Glucose')))

    ### following code throws an error ###

    spmf = Spmf("VMSP", spmf_bin_location_dir="./", input_direct=raw_seq,
             input_type="text", output_filename="output.txt", arguments=[0.5])

    spmf.run()

    cfm= CoreFlowMiner()
    root=cfm.getNewRootNode(Sequence.getSeqVolume(seq_list), seq_list)
    cfm.run(seq_list, "Meal", root, 5 * Sequence.getSeqVolume(seq_list)/100.0, Sequence.getSeqVolume(seq_list), [], {}, -1)

    x=json.dumps(root, ensure_ascii=False, default=TreeNode.json_serialize_dump, indent=1)
    print(x)
    
#main()

def run_spmf(sequence, attr, args=[0.5]):

    #convert input to list format
    if not isinstance(sequence, list):
            sequence=[sequence]
        
    raw_seq="\n".join(seqs.convertToVMSPReadable(attr) for seqs in sequence)

    spmf = Spmf("VMSP", spmf_bin_location_dir="./", input_direct=raw_seq,
             input_type="text", output_filename="output.txt", arguments=args)

    spmf.run()
    df=spmf.to_pandas_dataframe(pickle=True)

    with pd.option_context('display.max_rows', 10, 'display.max_columns', None):  # more options can be specified also
        print(df)


if __name__ == "__main__":
    #main()
    
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--file", help="File to read from",
                            type=str, default="sequence_braiding_refined.csv", required=False)
    argparser.add_argument("--evttype", help="1. Point 2.Interval 3.Mixed event",
                            type=int, default=1, required=False)
    argparser.add_argument("--startidx", help="Column Index of starting time",
                            type=int, default=0, required=False)
    argparser.add_argument("--endidx", help="Column Index of ending time",
                            type=int, default=1, required=False)
    argparser.add_argument("--format", help="Time format",
                            type=str, default="%m/%d/%y", required=False)
                            
    argparser.add_argument("--sep", help="separator of fields",
                            type=str, default=",", required=False)
    argparser.add_argument("--local", help="Local availability of file",
                            type=bool, default=True, required=False)
    argparser.add_argument("--spmf", help="Run spmf",
                            type=bool, default=False)

    argparser.add_argument("--attr", help="Attribute to run mining on",
                            type=str, required=True)

    argparser.add_argument("--output", help="Path of output file",
                            type=str, default="")



    args = argparser.parse_args()
    print(args)

    #Eventstore creates a list of events
    Es= EventStore()
    if(args.evttype==1):
        Es.importPointEvents(args.file, args.startidx, args.format, sep=args.sep, local=args.local)
    elif(args.evttype==2):
        Es.importIntervalEvents(args.file, args.startidx, args.endidx, args.format, sep=args.sep, local=args.local)
    else:
        Es.importMixedEvents(args.file, args.startidx, args.endidx, args.format, sep=args.sep, local=args.local)

    #create Sequences from Eventstore
    seq=Sequence(Es.events, Es)
    seq_list=Sequence.splitSequences(seq, "week")

    
    if(args.spmf==True):
        print("\n\n*****SPMF output******\n\n")
        run_spmf(seq_list, args.attr)
        print("\n\n")

    cfm= CoreFlowMiner()
    root=cfm.getNewRootNode(Sequence.getSeqVolume(seq_list), seq_list)
    cfm.run(seq_list, args.attr, root, 5 * Sequence.getSeqVolume(seq_list)/100.0, Sequence.getSeqVolume(seq_list), [], {}, -1)
    
    print("\n\n*****Coreflow output******\n\n")
    
    x=json.dumps(root, ensure_ascii=False, default=TreeNode.json_serialize_dump, indent=1)
    print(x)
    
    with open(args.output+'outfile.json', 'w') as the_file:
        the_file.write(x)




    
