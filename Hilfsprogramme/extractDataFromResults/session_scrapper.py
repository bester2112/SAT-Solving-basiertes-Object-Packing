import re

class Session:
    def __init__(self, date=None, time=None, folder1=None, folder2=None, filename=None, extension=None):
        self.date = date
        self.time = time
        self.folder1 = folder1
        self.folder2 = folder2
        self.filename = filename
        self.extension = extension

    def __str__(self):
        return f"Session: date={self.date}, time={self.time}, folder1={self.folder1}, folder2={self.folder2}, filename={self.filename}, extension={self.extension}"

    @staticmethod
    def process(filepath):
        with open(filepath, 'r') as f:
            for line in f:
                if "INFO: SessionName" in line:
                    match = re.search(
                        r"INFO: SessionName = (?P<date>\d{2}-\d{2}-\d{4})--(?P<time>\d{2}-\d{2})-(?P<folder1>\w+)__(?P<folder2>.+?)__(?P<filename>.+?)-txt",
                        line)
                    if match:
                        date = match.group('date').replace('-', '.')
                        time = match.group('time').replace('-', ':')
                        folder1 = match.group('folder1')
                        folder2 = match.group('folder2')
                        filename = match.group('filename')
                        extension = "txt"
                        return Session(date, time, folder1, folder2, filename, extension)




