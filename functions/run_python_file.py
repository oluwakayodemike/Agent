import subprocess
import os

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "executes a python file relative to the working directory with optional arguments and returns its output.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "the exact path of the python file to run, relative to the working directory.",
                },
                "args": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "an optional list of command line arguments to pass to the script",
                },      
            },
            "required": ["file_path"]
        },
    },
}

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        abs_working_path = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(abs_working_path, file_path))

        valid_target_dir = os.path.commonpath([abs_working_path, target_path]) == abs_working_path
        if valid_target_dir is False:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if os.path.isfile(target_path) is False:
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if target_path.endswith('.py') is False:
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_path]

        if args:
            command.extend(args)

        result = subprocess.run(command, cwd=abs_working_path, capture_output=True, text=True, timeout=30)

        output_str = ""
        if result.returncode != 0:
            output_str+= f"Process exited with code {result.returncode}\n"

        # checks if both ouputs are empty strings 
        if not result.stdout.strip() and not result.stderr.strip():
            output_str += "No output produced"
        else:
            output_str += f"STDOUT: {result.stdout}\n"
            output_str += f"STDERR: {result.stderr}"

        return output_str
    except Exception as e:
        return f"Error: executing Python file: {e}"