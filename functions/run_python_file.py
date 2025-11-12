import os
import subprocess
from google.genai import types


def run_python_file(working_directory, file_path, args=[]):
    full_path = os.path.join(working_directory, file_path)
    resolved_filepath = os.path.realpath(full_path)
    resolved_working_directory = os.path.realpath(working_directory)

    if not resolved_filepath.startswith(resolved_working_directory):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(resolved_filepath):
        return f'Error: File "{file_path}" not found.'

    if not resolved_filepath.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        output = []
        completed_process = subprocess.run(
            ["python3", resolved_filepath] + args,
            timeout=30,
            capture_output=True,
            text=True,
            cwd=resolved_working_directory,
        )
        if completed_process.stdout:
            output.append(f"STDOUT: \n{completed_process.stdout}")
        if completed_process.stderr:
            output.append(f"STDERR: \n{completed_process.stderr}")
        if completed_process.returncode != 0:
            output.append(
                f"Process exited with return code {completed_process.returncode}"
            )

        return "\n".join(output) if output else "No output produced."

    except Exception as e:
        return f"Error: executing Python file: {e}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a Python file and returns its output(stdout and stderr), constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The Python file, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Optional command-line arguments to pass to the Python script",
                items=types.Schema(type=types.Type.STRING),
            ),
        },
        required=["file_path"],
    ),
)
