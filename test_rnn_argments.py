import argparse

from rnn_recommend import add_argments2parser

def test_answer1():
    parser = add_argments2parser()
    args = parser.parse_args(
        ["--project", "MDT", "--window_size", "3", "--step", "10", "--lookup", "1000", "--batch_size", "32",
         "--epochs",  "500", "--threshold", "0.91", "--remove_dupe"])
    assert args.project == "MDT"

def test_answer2():
    parser = add_argments2parser()
    args = parser.parse_args(
        ["--project", "MDT", "--window_size", "3", "--step", "10", "--lookup", "1000", "--batch_size", "32",
         "--epochs",  "500", "--threshold", "0.91", "--remove_dupe"])
    assert args.various_window == False

def test_answer3():
    parser = add_argments2parser()
    args = parser.parse_args(
        ["--project", "MDT", "--window_size", "3", "--step", "10", "--lookup", "1000", "--batch_size", "32",
         "--epochs",  "500", "--threshold", "0.91", "--remove_dupe"])
    assert args.flexible_train == False

def test_answer4():
    parser = add_argments2parser()
    args = parser.parse_args(
        ["--project", "MDT", "--window_size", "3", "--step", "10", "--lookup", "1000", "--batch_size", "32",
         "--epochs",  "500", "--threshold", "0.91", "--remove_dupe"])
    assert args.flexible_test == False

def test_answer5():
    parser = add_argments2parser()
    args = parser.parse_args(
        ["--project", "MDT", "--window_size", "3", "--step", "10", "--lookup", "1000", "--batch_size", "32",
         "--epochs",  "500", "--threshold", "0.91", "--remove_dupe"])
    assert args.oversampling == 0

def test_answer6():
    parser = add_argments2parser()
    args = parser.parse_args(
        ["--project", "MDT", "--window_size", "3", "--step", "10", "--lookup", "1000", "--batch_size", "32",
         "--epochs",  "500", "--threshold", "0.91", "--remove_dupe"])
    assert args.remove_dupe == True

def test_answer7():
    parser = add_argments2parser()
    args = parser.parse_args(
        ["--project", "MDT", "--window_size", "3", "--step", "10", "--lookup", "1000", "--batch_size", "32",
         "--epochs",  "500", "--threshold", "0.91", "--remove_dupe"])
    assert args.window_size == 3

def test_answer8():
    parser = add_argments2parser()
    args = parser.parse_args(
        ["--project", "MDT", "--window_size", "3", "--step", "10", "--lookup", "1000", "--batch_size", "32",
         "--epochs", "500", "--threshold", "0.91", "--remove_dupe"])
    assert args.step == 10

def test_answer9():
    parser = add_argments2parser()
    args = parser.parse_args(
        ["--project", "MDT", "--window_size", "3", "--step", "10", "--lookup", "1000", "--batch_size", "32",
         "--epochs", "500", "--threshold", "0.91", "--remove_dupe"])
    assert args.lookup == 1000

def test_answer10(): #default value
    parser = add_argments2parser()
    args = parser.parse_args(
        ["--project", "MDT", "--window_size", "3", "--step", "10", "--lookup", "1000", "--batch_size", "32",
         "--epochs", "500", "--threshold", "0.91", "--remove_dupe"])
    assert args.embedding_size == 512

def test_answer11(): #default value
    parser = add_argments2parser()
    args = parser.parse_args(
        ["--project", "MDT", "--window_size", "3", "--step", "10", "--lookup", "1000", "--batch_size", "32",
         "--epochs", "500", "--threshold", "0.91", "--remove_dupe"])
    assert args.lstm_memory_cells == 256

def test_answer12():  # default value
    parser = add_argments2parser()
    args = parser.parse_args(
        ["--project", "MDT", "--window_size", "3", "--step", "10", "--lookup", "1000", "--batch_size", "32",
         "--epochs", "500", "--threshold", "0.91", "--remove_dupe"])
    assert args.lstm_dropout == 0

def test_answer13():  # default value
    parser = add_argments2parser()
    args = parser.parse_args(
        ["--project", "MDT", "--window_size", "3", "--step", "10", "--lookup", "1000", "--batch_size", "32",
         "--epochs", "500", "--threshold", "0.91", "--remove_dupe"])
    assert args.batch_size == 32

def test_answer13():  # default value
    parser = add_argments2parser()
    args = parser.parse_args(
        ["--project", "MDT", "--window_size", "3", "--step", "10", "--lookup", "1000", "--batch_size", "32",
         "--epochs", "500", "--threshold", "0.91", "--remove_dupe"])
    assert args.epochs == 500

def test_answer14():  # default value
    parser = add_argments2parser()
    args = parser.parse_args(
        ["--project", "MDT", "--window_size", "3", "--step", "10", "--lookup", "1000", "--batch_size", "32",
         "--epochs", "500", "--threshold", "0.91", "--remove_dupe"])
    assert args.threshold == 0.91

def test_answer15():  # default value
    parser = add_argments2parser()
    args = parser.parse_args(
        ["--project", "MDT", "--window_size", "3", "--step", "10", "--lookup", "1000", "--batch_size", "32",
         "--epochs", "500", "--threshold", "0.91", "--remove_dupe"])
    assert args.top_k == 10