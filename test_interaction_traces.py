import argparse

from rnn_recommend import add_argments2parser
from libs.interaction_traces import InteractionTraces

def test_answer11():
    parser = add_argments2parser()
    args = parser.parse_args(
        ["--project", "MDT", "--window_size", "3", "--step", "10", "--lookup", "1000", "--batch_size", "32",
         "--epochs",  "500", "--threshold", "0.91", "--remove_dupe"])
    directory_name = 'dataset/Project_{0}/'.format(args.project)
    interaction_traces = InteractionTraces(directory_name)
    assert interaction_traces.directory_name == "dataset/Project_MDT/"

def test_answer12():
    parser = add_argments2parser()
    args = parser.parse_args(
        ["--project", "MDT", "--window_size", "3", "--step", "10", "--lookup", "1000", "--batch_size", "32",
         "--epochs",  "500", "--threshold", "0.91", "--remove_dupe"])
    directory_name = 'dataset/Project_{0}/'.format(args.project)
    interaction_traces = InteractionTraces(directory_name)
    assert len(interaction_traces.interaction_trace_set) == 245

def test_answer13():
    parser = add_argments2parser()
    args = parser.parse_args(
        ["--project", "MDT", "--window_size", "3", "--step", "10", "--lookup", "1000", "--batch_size", "32",
         "--epochs",  "500", "--threshold", "0.91", "--remove_dupe"])
    directory_name = 'dataset/Project_{0}/'.format(args.project)
    interaction_traces = InteractionTraces(directory_name)
    assert len(interaction_traces.event_set) == 4081

def test_answer14():
    parser = add_argments2parser()
    args = parser.parse_args(
        ["--project", "MDT", "--window_size", "3", "--step", "10", "--lookup", "1000", "--batch_size", "32",
         "--epochs",  "500", "--threshold", "0.91", "--remove_dupe"])
    directory_name = 'dataset/Project_{0}/'.format(args.project)
    interaction_traces = InteractionTraces(directory_name)
    assert len(interaction_traces.edit_set) == 114

def test_answer15():
    parser = add_argments2parser()
    args = parser.parse_args(
        ["--project", "MDT", "--window_size", "3", "--step", "10", "--lookup", "1000", "--batch_size", "32",
         "--epochs",  "500", "--threshold", "0.91", "--remove_dupe"])
    directory_name = 'dataset/Project_{0}/'.format(args.project)
    interaction_traces = InteractionTraces(directory_name)
    assert len(interaction_traces.view_set) == 3967

def test_answer16():
    parser = add_argments2parser()
    args = parser.parse_args(
        ["--project", "MDT", "--window_size", "3", "--step", "10", "--lookup", "1000", "--batch_size", "32",
         "--epochs",  "500", "--threshold", "0.91", "--remove_dupe"])
    directory_name = 'dataset/Project_{0}/'.format(args.project)
    interaction_traces = InteractionTraces(directory_name)
    assert interaction_traces.interaction_trace_set[0].name == "MDT-264174-125525.xml"