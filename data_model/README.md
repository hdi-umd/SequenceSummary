# Creating Sequences

Given a list of Events splitted by some time or some other attribute value, we can create a list of sequence the following way.

    # Importing point events from an example dataset
    sequence_braiding = EventStore.importPointEvents(Path_to_csv, 0, "%m/%d/%y", sep=',', local=True)

    # Here sequence_braiding is a list of events
    sequence_braiding_split=EventStore.splitSequences(sequence_braiding, "week")
    seq_list=[]
    for seqs in sequence_braiding_split:
        seq_list.append(Sequence(seqs))
    # create a dictionary mapping attribute values to unicode    
    Sequence.create_attr_dict(seq_list)

    # Convert the attribute values to a VMSP readable string
    raw_seq="\n".join( seqs.convertToVMSPReadable('Meal') for seqs in seq_list)
    # Initiate spmf
    spmf = Spmf("VMSP", spmf_bin_location_dir="./test_files/", input_direct=raw_seq,
             input_type="text", output_filename="output.txt", arguments=[0.5])
    spmf.run()
    print(spmf.to_pandas_dataframe(pickle=True))
    
