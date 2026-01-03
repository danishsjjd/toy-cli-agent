import os


def is_in_working_dir(working_directory: str, path: str):
    working_dir_abs = os.path.abspath(working_directory)
    target_path = os.path.normpath(os.path.join(working_dir_abs, path))
    valid_target_path = (
        os.path.commonpath([working_dir_abs, target_path]) == working_dir_abs
    )

    return valid_target_path, target_path
