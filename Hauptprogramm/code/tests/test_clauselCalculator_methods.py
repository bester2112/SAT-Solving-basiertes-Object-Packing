import src._clauselCalculator as c


def test_fileparser_calculate_time():
    """
    Test the fileparser module
    """
    clauselCalculator = c.ClauselCalculator("", "", "", "", "")
    time = []
    text = []
    time.append(982043.369)
    text.append("Runtime: TotalSec: 982043.369 == 23.369 seconds, 47 minutes, 08 hours, 11 days")
    time.append(539944.894)
    text.append("Runtime: TotalSec: 539944.894 == 04.894 seconds, 59 minutes, 05 hours, 06 days")
    time.append(899652.101)
    text.append("Runtime: TotalSec: 899652.101 == 12.101 seconds, 54 minutes, 09 hours, 10 days")
    time.append(357663.126)
    text.append("Runtime: TotalSec: 357663.126 == 03.126 seconds, 21 minutes, 03 hours, 04 days")
    time.append(206656.641)
    text.append("Runtime: TotalSec: 206656.641 == 16.641 seconds, 24 minutes, 09 hours, 02 days")
    time.append(662404.111)
    text.append("Runtime: TotalSec: 662404.111 == 04.111 seconds, 00 minutes, 16 hours, 07 days")
    time.append(449166.888)
    text.append("Runtime: TotalSec: 449166.888 == 06.888 seconds, 46 minutes, 04 hours, 05 days")
    time.append(826374.420)
    text.append("Runtime: TotalSec: 826374.420 == 54.420 seconds, 32 minutes, 13 hours, 09 days")
    time.append(779312.463)
    text.append("Runtime: TotalSec: 779312.463 == 32.463 seconds, 28 minutes, 00 hours, 09 days")
    time.append(86399999.999)
    text.append("Runtime: TotalSec: 86399999.999 == 59.999 seconds, 59 minutes, 23 hours, 999 days")
    time.append(13.795)
    text.append("Runtime: TotalSec: 13.795 == 13.795 seconds, 00 minutes, 00 hours, 00 days")

    assert clauselCalculator.calculate_time(time[0]) == text[0]
    assert clauselCalculator.calculate_time(time[1]) == text[1]
    assert clauselCalculator.calculate_time(time[2]) == text[2]
    assert clauselCalculator.calculate_time(time[3]) == text[3]
    assert clauselCalculator.calculate_time(time[4]) == text[4]
    assert clauselCalculator.calculate_time(time[5]) == text[5]
    assert clauselCalculator.calculate_time(time[6]) == text[6]
    assert clauselCalculator.calculate_time(time[7]) == text[7]
    assert clauselCalculator.calculate_time(time[8]) == text[8]
    assert clauselCalculator.calculate_time(time[9]) == text[9]
    assert clauselCalculator.calculate_time(time[10]) == text[10]