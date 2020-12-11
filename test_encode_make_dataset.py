
from libs.interaction_traces import InteractionTraces
from libs.utils import make_dataset, integer_encode, integer_encode_without_zero_index

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
    num_categories = len(interaction_traces.edit_set)
    assert num_categories == 114