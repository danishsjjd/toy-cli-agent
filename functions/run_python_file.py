import os
import subprocess

from google.genai import types

from utils import is_in_working_dir


def run_python_file(working_directory, file_path, args=None):
    try:
        is_valid_path, target_file_path = is_in_working_dir(
            working_directory, file_path
        )

        if not is_valid_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if file_path[-3:] != ".py":
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_file_path]

        if args:
            command.extend(args)

        process = subprocess.run(
            command,
            timeout=30,
            text=True,
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
        )

        if process.returncode != 0:
            return "Process exited with code X"

        content = ""

        if process.stdout:
            content += f"STDOUT: {process.stdout}"

        if process.stderr:
            content += f"STDERR: {process.stderr}"

        if content == "":
            return "No output produced"

        return content
    except Exception as e:
        f"Error: executing Python file: {e}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run python code by specifying file path relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Python file path to run python code",
            ),
            "args": types.Schema(
                type=types.Type.OBJECT,
                description="Optional argument to run command",
                default=None,
            ),
        },
    ),
)
