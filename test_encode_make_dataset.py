
from libs.interaction_traces import InteractionTraces
from libs.makedataset import make_dataset, integer_encode, integer_encode_without_zero_index

def test_answer201():
    interaction_traces = InteractionTraces("dataset/Project_MDT/")
    file_indexes = integer_encode_without_zero_index(interaction_traces.event_set)
    num_file = len(file_indexes) + 1
    assert num_file == 4082

def test_answer202():
    interaction_traces = InteractionTraces("dataset/Project_MDT/")
    file_indexes = integer_encode_without_zero_index(interaction_traces.event_set)
    assert file_indexes[('view', '/.classpath')] == 1

def test_answer203():
    interaction_traces = InteractionTraces("dataset/Project_MDT/")
    category = integer_encode(interaction_traces.edit_set)
    num_categories = len(interaction_traces.edit_set)
    assert num_categories == 114

def test_answer204():
    interaction_traces = InteractionTraces("dataset/Project_MDT/")
    categories = integer_encode(interaction_traces.edit_set)
    assert categories['/DiagramEditPart.xpt'] == 0

def test_answer205():
    import numpy as np
    from keras.preprocessing import sequence
    from libs.interaction_traces import InteractionTraces

    # directory of interaction traces
    directory_name = 'dataset/Project_ECF/'
    interaction_trace_set = InteractionTraces(directory_name)
    trace = interaction_trace_set.interaction_trace_set[1]
    file_indexes = integer_encode_without_zero_index(interaction_trace_set.event_set)
    category_indexes = integer_encode(interaction_trace_set.edit_set)

    x_train, y_train = make_dataset(trace, file_indexes, category_indexes, window_size=4, step=5, lookup=30, is_remove_dupe=False)
    assert len(x_train) == 5 and len(x_train[0]) == 4

def test_answer206():
    import numpy as np
    from keras.preprocessing import sequence
    from libs.interaction_traces import InteractionTraces

    # directory of interaction traces
    directory_name = 'dataset/Project_ECF/'
    interaction_trace_set = InteractionTraces(directory_name)
    trace = interaction_trace_set.interaction_trace_set[1]
    file_indexes = integer_encode_without_zero_index(interaction_trace_set.event_set)
    category_indexes = integer_encode(interaction_trace_set.edit_set)

    x_train, y_train = make_dataset(trace, file_indexes, category_indexes, window_size=4, step=5, lookup=30, is_remove_dupe=False)
    assert len(y_train) == 5 and len(y_train[0]) == 3

