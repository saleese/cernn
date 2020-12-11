from libs.interaction_traces import InteractionTraces

import os
from libs.readfile import read

def test_answer101():
    interaction_traces = InteractionTraces("dataset/Project_MDT/")
    assert interaction_traces.directory_name == "dataset/Project_MDT/"

def test_answer102():
    interaction_traces = InteractionTraces("dataset/Project_MDT/")
    assert len(interaction_traces.interaction_trace_set) == 245

def test_answer103():
    interaction_traces = InteractionTraces("dataset/Project_MDT/")
    assert len(interaction_traces.event_set) == 4081

def test_answer104():
    interaction_traces = InteractionTraces("dataset/Project_MDT/")
    assert len(interaction_traces.edit_set) == 114

def test_answer105():
    interaction_traces = InteractionTraces("dataset/Project_MDT/")
    assert len(interaction_traces.view_set) == 3967

def test_answer106():
    interaction_traces = InteractionTraces("dataset/Project_MDT/")
    assert interaction_traces.interaction_trace_set[0].name == "MDT-264174-125525.xml"

def test_answer107():
    interaction_trace_i = read("dataset/Project_MDT/MDT-264174-125525.xml")
    assert interaction_trace_i.name == "MDT-264174-125525.xml"

def test_answer108():
    interaction_trace_i = read("dataset/Project_MDT/MDT-264174-125525.xml")
    assert len(interaction_trace_i.event_list) == 15

def test_answer108_1():
    interaction_trace_i = read("dataset/Project_MDT/MDT-264174-125525.xml")
    assert interaction_trace_i.event_list[0].filename == "/DiagramUpdater.xpt"

def test_answer109():
    interaction_trace_i = read("dataset/Project_MDT/MDT-264174-125525.xml")
    assert interaction_trace_i.num_events == 15

def test_answer110():
    interaction_trace_i = read("dataset/Project_MDT/MDT-264174-125525.xml")
    assert interaction_trace_i.event_list_names[0] == '/DiagramUpdater.xpt'

def test_answer111():
    interaction_trace_i = read("dataset/Project_MDT/MDT-264174-125525.xml")
    assert interaction_trace_i.event_tuple_list[0] == ('view', '/DiagramUpdater.xpt')

def test_answer112():
    interaction_trace_i = read("dataset/Project_MDT/MDT-264174-125525.xml")
    assert interaction_trace_i.event_tuple_list_groupby[0] == ('view', '/DiagramUpdater.xpt')

def test_answer113():
    interaction_trace_i = read("dataset/Project_MDT/MDT-264174-125525.xml")
    assert interaction_trace_i.event_tuple_list_groupby[0] == ('view', '/DiagramUpdater.xpt')

def test_answer114():
    interaction_trace_i = read("dataset/Project_MDT/MDT-264174-125525.xml")
    assert interaction_trace_i.event_tuple_set == [('view', '/DiagramUpdater.xpt'), ('view', '/mutatingUtils.ext')]

def test_answer115():
    interaction_trace_i = read("dataset/Project_MDT/MDT-264174-125525.xml")
    assert interaction_trace_i.view_set == ['/DiagramUpdater.xpt', '/mutatingUtils.ext']

def test_answer116():
    interaction_trace_i = read("dataset/Project_MDT/MDT-264174-125525.xml")
    assert interaction_trace_i.edit_set == []