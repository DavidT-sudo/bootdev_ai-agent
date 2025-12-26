import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    abs_working_directory = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    
    valid_file_path = os.path.commonpath([abs_working_directory, abs_file_path]) == abs_working_directory

    if not valid_file_path:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory\n'

    if not os.path.isfile(abs_file_path):
        return f'Error: "{file_path}" does not exist or is not a regular file\n'
    
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file'
    
    output = ""

    try:
        command = ["python", abs_file_path]
        if args:
            command.extend(args)
        
        process = subprocess.run(command, check=True, text=True, capture_output=True, timeout=30, cwd=abs_working_directory)

        if process.returncode != 0:
            return f'Error: Process exited with code {process.returncode}\n{process.stderr}\n'
        
        if not process.stdout and not process.stderr:
            output += f'No output produced\n'
        
        output += f'STDOUT: {process.stdout}\nSTDERR: {process.stderr}\n'

        return output
    
    except Exception as e:
        return f"Error: executing Python file: {e}"
    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a Python file, constrained to the working directory. Returns the stdout and stderr of the subprocess.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "working_directory": types.Schema(
                type=types.Type.STRING,
                description="The working directory.",
            ),
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the Python file to run, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Arguments to pass to the Python file.",
                ),
                description="Arguments to pass to the Python file.",
            ),
        },
    ),
)