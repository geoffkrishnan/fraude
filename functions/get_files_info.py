import os

def get_files_info(working_directory, directory="."):
    absolute_path = os.path.join(working_directory, directory)
    if not absolute_path.startswith(''
    return f'Error: Cannot list {directory} as it outside the permitted working directory') 
    if type(directory) == str:
        return f'Error: "{directory}" is not a directory'
    



