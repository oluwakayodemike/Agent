import os

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        abs_working_path = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(abs_working_path, directory))
    
        valid_target_dir = os.path.commonpath([abs_working_path, target_dir]) == abs_working_path
        if valid_target_dir is False:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
            
        if os.path.isdir(target_dir) is False:
            return f'Error: "{directory}" is not a directory'
            
        if os.path.isdir(target_dir) is True:
            return f'Success: "{directory}" is within the working directory'
    except Exception as e:
        return f"Error: {e}"