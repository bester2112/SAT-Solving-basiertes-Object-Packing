import os


class ExecutionCheck:
    def __init__(self, execute_file_path=None, image_folder_exists=None, files_exist=None, file_problem_file_size=None,
                 file_problem_size_formated=None):
        self.execute_file_path = execute_file_path
        self.image_folder_exists = image_folder_exists
        self.files_exist = files_exist
        self.file_problem_file_size = file_problem_file_size
        self.file_problem_size_formated = file_problem_size_formated

    def __str__(self):
        return f"ExecutionCheck: execute_file_path={self.execute_file_path}, image_folder_exists={self.image_folder_exists}, files_exist={self.files_exist}, file_problem_file_size={self.file_problem_file_size}, file_problem_size_formated={self.file_problem_size_formated}"

    @staticmethod
    def process(filepath, argparser, image):
        file_problem_file_size = None
        file_problem_size_formated = None
        if argparser and (not image):
            with open('missing-results.txt', 'a') as f:
                f.write(f"{argparser.execute_file_path}\n")
            return ExecutionCheck(argparser.execute_file_path, False, False)

        if argparser and image:
            image_folder_exists = os.path.exists(image.image_folder)
            files_exist = False
            required_files = ["_file_problem.cnf", "_file_problem.cnf.res", "_finalSolution.png", "collected_info.txt"]
            if image_folder_exists:
                files_in_folder = os.listdir(image.image_folder)
                files_exist = all(file in files_in_folder for file in required_files)

                for file_name in ["_file_problem.cnf", "_file_problem.cnf.res"]:
                    if file_name in files_in_folder:
                        with open(os.path.join(image.image_folder, file_name), 'r') as f:
                            for line in f:
                                if 'file_size:' in line:
                                    file_problem_file_size = int(line.split(':')[1].strip())
                                elif 'file_size_formated:' in line:
                                    file_problem_size_formated = line.split(':')[1].strip()

            with open('existing-results.txt' if files_exist else 'missing-results.txt', 'a') as f:
                if "benchmark_2/" in argparser.execute_file_path:
                    argparser.execute_file_path = argparser.execute_file_path.replace("benchmark_2/", "benchmark/")
                f.write(f"{argparser.execute_file_path}\n")

            return ExecutionCheck(argparser.execute_file_path, image_folder_exists, files_exist,
                                  file_problem_file_size, file_problem_size_formated)

