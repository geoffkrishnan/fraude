import os
from config import MAX_CHARS


def get_file_content(working_directory, file_path):
    full_path = os.path.join(working_directory, file_path)
    resolved_filepath = os.path.realpath(full_path)
    resolved_working_directory = os.path.realpath(working_directory)

    if not resolved_filepath.startswith(resolved_working_directory):
        return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(resolved_filepath):
        return f'Error: "{resolved_filepath}" is not found or is not a regular file: {resolved_filepath}'

    try:
        with open(resolved_filepath, "r") as f:
            char_count = sum(len(line) for line in f)
            f.seek(0)

            if char_count > MAX_CHARS:
                file_content_string = f.read(MAX_CHARS)
                file_content_string += f'[...File "{resolved_filepath}" truncated at {MAX_CHARS} characters]'
                return file_content_string
            else:
                file_content_string = f.read()
                return file_content_string
    except Exception as e:
        return f'Error reading file "{resolved_filepath}": as {e}'
