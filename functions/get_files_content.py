import os
import config

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "reads the text content of a specified file relative to the working directory.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "the exact path of the file to read, relative to the working directory.",
                },
            },
            "required": ["file_path"]
        },
    },
}

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        abs_working_path = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(abs_working_path, file_path))

        valid_target_dir = os.path.commonpath([abs_working_path, target_path]) == abs_working_path
        if valid_target_dir is False:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if os.path.isfile(target_path) is False:
            return f'Error: File not found or is not a regular file: "{file_path}"'


        with open(target_path, "r", encoding="utf-8", errors="replace") as file:
            content = file.read(config.MAX_CHARS)

            if file.read(1):
                content += f'[...File "{file_path}" truncated at {config.MAX_CHARS} characters]'

            return content
    except Exception as e:
        return f"Error: {e}"