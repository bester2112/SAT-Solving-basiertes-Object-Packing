import src._fileparser as f

def test_fileparser_init_with_values():
    """
    Test the fileparser module
    """
    argParse_filename = "benchmark18-01-2023--11-17-9.txt"
    argParse_timeLimit = "30000"
    argParse_debugMode = False
    fileparser = f.FileParser(fileName=argParse_filename,
                              timeLimit=argParse_timeLimit,
                              debugMode=argParse_debugMode)
    assert fileparser.fileName == argParse_filename
    assert fileparser.timeLimit == argParse_timeLimit
    assert fileparser.debugMode == argParse_debugMode
    assert fileparser.allSpielsteine == []
    assert fileparser.height == -1
    assert fileparser.width == -1

def test_fileparser_init_without_values():
    fileparser = f.FileParser()
    assert fileparser.fileName == ""
    assert fileparser.timeLimit == ""
    assert fileparser.debugMode == False
    assert fileparser.allSpielsteine == []
    assert fileparser.height == -1
    assert fileparser.width == -1





