import os

from google.genai import types

from config import MAX_CHARS
from utils import is_in_working_dir


def get_file_content(working_directory, file_path):
    try:
        valid_target_dir, target_file = is_in_working_dir(working_directory, file_path)
        if not valid_target_dir:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        file_content_string = ""
        with open(target_file, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if f.read(1):
                file_content_string += (
                    f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                )

        return file_content_string

    except Exception as e:
        return f"Error {e}"


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read file contents in a specified file path relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to read content from",
            ),
        },
    ),
)
