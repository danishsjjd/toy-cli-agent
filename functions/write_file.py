import os
from pathlib import Path

from google.genai import types

from utils import is_in_working_dir


def write_file(working_directory, file_path, content):
    try:
        is_valid_path, target_path = is_in_working_dir(working_directory, file_path)
        if not is_valid_path:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        if os.path.isdir(target_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        directory = Path(target_path).parent

        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)

        with open(target_path, "w") as f:
            f.write(content)

        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )
    except Exception as e:
        return f"Error: {e}"


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write content to file in a specified file path relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to write content in",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content of the file to write",
            ),
        },
    ),
)
