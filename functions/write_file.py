import os
from google.genai import types


def write_file(working_directory, file_path, content):
    full_path = os.path.join(working_directory, file_path)
    resolved_filepath = os.path.realpath(full_path)
    resolved_working_directory = os.path.realpath(working_directory)

    if not resolved_filepath.startswith(resolved_working_directory):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(resolved_filepath):
        try:
            os.makedirs(os.path.dirname(resolved_filepath), exist_ok=True)
        except Exception as e:
            return f"Error: creating directory: {e}"
    if os.path.exists(resolved_filepath) and os.path.isdir(resolved_filepath):
        return f'Error: "{file_path}" is a directory, not  file'
    try:
        with open(resolved_filepath, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error writing file "{file_path}": {e}'


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes or overwrites contents of a file to working directory. If the file/file path's directories don't exist, creates them. Constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to write content to, constrained to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file.",
            ),
        },
        required=["file_path", "content"],
    ),
)
