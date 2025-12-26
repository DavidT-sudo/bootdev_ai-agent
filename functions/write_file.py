import os
from google.genai import types

def write_file(working_directory, file_path, content):
    abs_working_directory = os.path.abspath(working_directory)
    abs_target_dir = os.path.abspath(os.path.join(working_directory, file_path))
    
    valid_target_dir = os.path.commonpath([abs_working_directory, abs_target_dir]) == abs_working_directory

    if not valid_target_dir:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory\n'

    if os.path.isdir(abs_target_dir):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory\n'

    os.makedirs(os.path.dirname(abs_target_dir), exist_ok=True)

    try:
        with open(abs_target_dir, 'w') as file:
            file.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)\n'
    except Exception as e:
        return f'Error: {str(e)}\n'

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes contents to a file, constrained to the working directory. Returns the number of characters written. Also overwrites any previous words.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "working_directory": types.Schema(
                type=types.Type.STRING,
                description="The working directory.",
            ),
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write to, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file.",
            ),
        },
    ),
)