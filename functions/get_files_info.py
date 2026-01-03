import os

from google.genai import types

from utils import is_in_working_dir


def get_files_info(working_directory: str, directory="."):
    try:
        valid_target_dir, target_dir = is_in_working_dir(working_directory, directory)
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        content = ""

        for item in os.listdir(target_dir):
            item_path = os.path.join(target_dir, item)
            content += f"- {item} file_size={os.path.getsize(item_path)} bytes, is_dir={"True" if os.path.isdir(item_path) else "False"}\n"

        return content
    except Exception as e:
        return f"Error: {e}"


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)
