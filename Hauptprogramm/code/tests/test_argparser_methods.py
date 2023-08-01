import pytest

import src._argparser as a


def test_parse_inputfile_only():
    argparser = a.ArgParser()
    inputfile = "inputFile.txt"
    args = argparser.parse_args([inputfile])
    assert args.filename == argparser.fileName
    assert args.filename == inputfile


def test_parse_missing_inputfile():
    with pytest.raises(SystemExit):
        argparser = a.ArgParser()
        argparser.parse_args([])


def test_parse_runtime_written_as_text():
    with pytest.raises(SystemExit):
        argparser = a.ArgParser()
        inputfile = "inputFile.txt"
        runtime = "ten"
        argparser.parse_args([inputfile, "-s", runtime])


def test_parse_inputfile_and_runtime():
    argparser = a.ArgParser()
    inputfile = "inputFile.txt"
    runtime = "10"
    args = argparser.parse_args([inputfile, "-s", runtime])
    assert args.filename == argparser.fileName
    assert args.filename == inputfile
    assert args.seconds == argparser.timeLimit
    assert args.seconds == int(runtime)


def test_parse_inputfile_and_runtime_alternative():
    argparser = a.ArgParser()
    inputfile = "inputFile.txt"
    runtime = "100"
    args = argparser.parse_args([inputfile, "--seconds", runtime])
    assert args.filename == argparser.fileName
    assert args.filename == inputfile
    assert args.seconds == argparser.timeLimit
    assert args.seconds == int(runtime)


def test_parse_inputfile_and_runtime_wrong_case():
    argparser = a.ArgParser()
    inputfile = "inputFile.txt"
    runtime = "10"
    args = argparser.parse_args([inputfile, "-s", runtime])
    assert args.filename == argparser.fileName
    assert args.filename == inputfile
    assert args.seconds == argparser.timeLimit
    assert args.seconds != str(runtime)
