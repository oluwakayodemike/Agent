import os

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        abs_working_path = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(abs_working_path, directory))
    
        valid_target_dir = os.path.commonpath([abs_working_path, target_dir]) == abs_working_path
        if valid_target_dir is False:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
            
        if os.path.isdir(target_dir) is False:
            return f'Error: "{directory}" is not a directory'

        # for items in this directory
        # get name, file size, where it is a directory
        result = []
        for item in os.listdir(target_dir):
            full_item_path = os.path.join(target_dir, item)
            
            is_dir = os.path.isdir(full_item_path)
            file_size = os.path.getsize(full_item_path)
            result.append(f"- {item}: file_size={file_size}, is_dir={is_dir}")

        return '\n'.join(result)
    except Exception as e:
        return f"Error: {e}"