import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from EventStore import EventStore
from Pattern import Pattern
from SentenTreeMiner import SentenTreeMiner
from Sequence import Sequence
from TreeNode import TreeNode, GraphNode
import pandas as pd
from IPython.display import display
import json
import argparse



if __name__ == "__main__":
    #main()
    
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--file", help="File to read from",
                            type=str, default="../coreflow/sequence_braiding_refined.csv", required=False)
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

    stm= SentenTreeMiner()
    #cfm.truncateSequences(self, seqs, hashval, evtAttr, node,trailingSeqSegs, notContain)
    root=GraphNode()
    root.incomingSequences=seq_list
    visibleGroups=stm.expandSeqTree("Meal",root,  expandCnt=30, minSupport=1, maxSupport=len(seq_list))
    
    
    print("\n\n*****SentenTree output******\n\n")
    
    x=json.dumps(root, ensure_ascii=False, default=GraphNode.json_serialize_dump, indent=1)
    print(x)

    with open(args.output+'outfile.json', 'w') as the_file:
        the_file.write(x)


