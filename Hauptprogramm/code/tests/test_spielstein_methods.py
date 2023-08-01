import pytest

import src._spielstein as s

def test_spielstein_wrong_file():
    # Datei format passt nicht
    # #
    # ##
    # sollte sein:
    # #.
    # ##
    blocks = [[1], [1, 1]]
    with pytest.raises(ValueError):
        s.Spielstein(blocks)

def test_spielstein_right_file():
    # #.
    # ##
    blocks = [[1, 1], [1, 1]]
    spielstein = s.Spielstein(blocks)
    if spielstein.all_equal(blocks):
        assert True
    else:
        assert False
    assert spielstein.height == 2
    assert spielstein.width == 2
    assert spielstein.list2D == [[1, 1], [1, 1]]
    assert spielstein.firstPixelList == []
    assert spielstein.moeglichePositionen == []
    assert spielstein.alleMoeglichenPlaziertenSteine == {}
    assert spielstein.equivalentClauselList == []
    assert spielstein.spielsteineImSpiel == -1


