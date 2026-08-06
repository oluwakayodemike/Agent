import subprocess
import os

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