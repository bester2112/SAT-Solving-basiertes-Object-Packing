import src._main as m


def test_create_default_log_folder():
    result = m.create_log_folder()
    assert ("folder already exists." in result) == True


def test_create_session_name_empty():
    inputString = ""
    result = m.create_session_name(inputString)
    assert is_valid_pattern(result) == True


def test_create_session_name_simple_input():
    inputString = "benchmark18-01-2023--11-17-9.txt"
    result = m.create_session_name(inputString)
    assert is_valid_pattern(result) == True


def test_create_session_name_folder_input():
    inputString = "folder1/filename19-01-2023--11-17-9.txt"
    result = m.create_session_name(inputString)
    assert is_valid_pattern(result) == True


def test_create_sessoion_name_multiple_folder_input():
    inputString = "folder1/folder2/folder3/filename19-01-2023--11-17-9.txt"
    result = m.create_session_name(inputString)
    assert is_valid_pattern(result) == True


def is_valid_pattern(string):
    pattern = "XX-XX-XXXX--XX-XX"
    pattern_length = len(pattern)

    for i in range(len(string) - pattern_length + 1):
        sub_string = string[i:i + pattern_length]
        if len(sub_string) != pattern_length:
            continue
        match = True
        for j in range(pattern_length):
            if pattern[j] == 'X':
                if not sub_string[j].isdigit():
                    match = False
                    break
            elif sub_string[j] != pattern[j]:
                match = False
                break
        if match:
            return True
    return False


def test_is_valid_pattern():
    string = "ertgertgergedrgerg/11-22-3333--44-55dfgrdztgertgdefgerg"
    assert is_valid_pattern(string) == True

    string = "11-22-3333--44-55"
    assert is_valid_pattern(string) == True

    string = "11-22-333--44-55"
    assert is_valid_pattern(string) == False

    string = "11-22-3333-44-55"
    assert is_valid_pattern(string) == False

    string = "11-22-3333--44-5A"
    assert is_valid_pattern(string) == False
