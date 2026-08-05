import os

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        abs_working_path = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(abs_working_path, file_path))

        valid_target_path = os.path.commonpath([abs_working_path, target_path]) == abs_working_path
        if valid_target_path is False:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        # points to an existing dir?
        if os.path.isdir(target_path) is True:
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        # creates nested directories, exist_ok prevents crash if folder already exists. 
        # only creates dir up to the file's parent folder
        parent_dir = os.path.dirname(target_path)
        os.makedirs(parent_dir, exist_ok=True)

        with open(target_path, "w", encoding="utf-8") as file:
            file.write(content)

            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"