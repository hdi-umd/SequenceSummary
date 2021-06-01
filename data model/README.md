# Creating Sequences

Given a list of Events splitted by some time or some other attribute value, we can create a list of sequence the following way.

    # Here sequence_braiding is a list of events
    sequence_braiding_split=EventStore.splitSequences(sequence_braiding, "week")
    seq_list=[]
    for seqs in sequence_braiding_split:
        seq_list.append(Sequence(seqs))
    # create a dictionary mapping attribute values to unicode    
    Sequence.create_attr_dict(seq_list)
