import os
from google.genai import types


def get_files_info(working_directory, directory="."):
    full_path = os.path.join(working_directory, directory)
    resolved_path = os.path.realpath(full_path)
    resolved_working_directory = os.path.realpath(working_directory)

    if not resolved_path.startswith(resolved_working_directory):
        return f'\tError: Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.isdir(resolved_path):
        return f'\tError: "{directory}" is not a directory'

    try:
        dir_list = []
        for item in os.listdir(resolved_path):
            if item.startswith(".") or item == "__pycache__":
                continue
            item_path = os.path.join(resolved_path, item)
            dir_list.append(
                f" - {item}: file_size={os.path.getsize(item_path)} bytes, is_dir={os.path.isdir(item_path)}"
            )
        return "\n".join(dir_list)
    except Exception as e:
        return f"Error listing files: {e}"


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
        required=["directory"],
    ),
)
