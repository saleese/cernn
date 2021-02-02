import argparse

from rnn_recommend import add_argments2parser

def test_answer001():
    parser = add_argments2parser()
    args = parser.parse_args(
        ["--project", "MDT", "--window_size", "3", "--step", "10", "--lookup", "1000", "--batch_size", "32",
         "--epochs",  "500", "--threshold", "0.91", "--remove_dupe"])
    assert args.project == "MDT"

def test_answer006():
    parser = add_argments2parser()
    args = parser.parse_args(
        ["--project", "MDT", "--window_size", "3", "--step", "10", "--lookup", "1000", "--batch_size", "32",
         "--epochs",  "500", "--threshold", "0.91", "--remove_dupe"])
    assert args.remove_dupe == True

def test_answer007():
    parser = add_argments2parser()
    args = parser.parse_args(
        ["--project", "MDT", "--window_size", "3", "--step", "10", "--lookup", "1000", "--batch_size", "32",
         "--epochs",  "500", "--threshold", "0.91", "--remove_dupe"])
    assert args.window_size == 3

def test_answer008():
    parser = add_argments2parser()
    args = parser.parse_args(
        ["--project", "MDT", "--window_size", "3", "--step", "10", "--lookup", "1000", "--batch_size", "32",
         "--epochs", "500", "--threshold", "0.91", "--remove_dupe"])
    assert args.step == 10

def test_answer009():
    parser = add_argments2parser()
    args = parser.parse_args(
        ["--project", "MDT", "--window_size", "3", "--step", "10", "--lookup", "1000", "--batch_size", "32",
         "--epochs", "500", "--threshold", "0.91", "--remove_dupe"])
    assert args.lookup == 1000

def test_answer010(): #default value
    parser = add_argments2parser()
    args = parser.parse_args(
        ["--project", "MDT", "--window_size", "3", "--step", "10", "--lookup", "1000", "--batch_size", "32",
         "--epochs", "500", "--threshold", "0.91", "--remove_dupe"])
    assert args.embedding_size == 512

def test_answer011(): #default value
    parser = add_argments2parser()
    args = parser.parse_args(
        ["--project", "MDT", "--window_size", "3", "--step", "10", "--lookup", "1000", "--batch_size", "32",
         "--epochs", "500", "--threshold", "0.91", "--remove_dupe"])
    assert args.lstm_memory_cells == 256

def test_answer012():  # default value
    parser = add_argments2parser()
    args = parser.parse_args(
        ["--project", "MDT", "--window_size", "3", "--step", "10", "--lookup", "1000", "--batch_size", "32",
         "--epochs", "500", "--threshold", "0.91", "--remove_dupe"])
    assert args.lstm_dropout == 0

def test_answer013():  # default value
    parser = add_argments2parser()
    args = parser.parse_args(
        ["--project", "MDT", "--window_size", "3", "--step", "10", "--lookup", "1000", "--batch_size", "32",
         "--epochs", "500", "--threshold", "0.91", "--remove_dupe"])
    assert args.batch_size == 32

def test_answer014():  # default value
    parser = add_argments2parser()
    args = parser.parse_args(
        ["--project", "MDT", "--window_size", "3", "--step", "10", "--lookup", "1000", "--batch_size", "32",
         "--epochs", "500", "--threshold", "0.91", "--remove_dupe"])
    assert args.epochs == 500

def test_answer015():  # default value
    parser = add_argments2parser()
    args = parser.parse_args(
        ["--project", "MDT", "--window_size", "3", "--step", "10", "--lookup", "1000", "--batch_size", "32",
         "--epochs", "500", "--threshold", "0.91", "--remove_dupe"])
    assert args.threshold == 0.91

def test_answer016():  # default value
    parser = add_argments2parser()
    args = parser.parse_args(
        ["--project", "MDT", "--window_size", "3", "--step", "10", "--lookup", "1000", "--batch_size", "32",
         "--epochs", "500", "--threshold", "0.91", "--remove_dupe"])
    assert args.top_k == 10