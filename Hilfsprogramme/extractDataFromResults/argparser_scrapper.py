
class Argparser:
    def __init__(self, execute_file_path=None, time_limit=None, model=None):
        self.execute_file_path = execute_file_path
        self.time_limit = time_limit
        self.model = model

    def __str__(self):
        return f"Argparser: execute_file_path={self.execute_file_path}, time_limit={self.time_limit}, model={self.model}"

    @staticmethod
    def process(filepath):
        with open(filepath, 'r') as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                if "INFO: -Argparser-" in line:
                    execute_file_path, time_limit, model = None, None, None
                    if "DEBUG: argParser.fileName" in lines[i+1]:
                        execute_file_path = lines[i+1].split()[-1]
                    if "DEBUG: argParser.timeLimit" in lines[i+2]:
                        time_limit = lines[i+2].split()[-1]
                    if "DEBUG: argParser.model" in lines[i+3]:
                        model = lines[i+3].split('.')[-1]
                    return Argparser(execute_file_path, time_limit, model)