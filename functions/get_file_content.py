from config import MAX_CHARS
import os
from google.genai import types

def get_file_content(working_directory, file_path):
    abs_working_directory = os.path.abspath(working_directory)
    abs_target_dir = os.path.abspath(os.path.join(working_directory, file_path))
    
    # Will be True or False
    valid_target_dir = os.path.commonpath([abs_working_directory, abs_target_dir]) == abs_working_directory

    if not valid_target_dir:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory\n'

    if not os.path.isfile(abs_target_dir):
        return f'Error: File not found or is not a regular file: "{file_path}"\n'

    try:
        with open(abs_target_dir, 'r') as file:
            contents = file.read(MAX_CHARS)
            if file.read(1) != "":
                contents += f'\n[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            
            return contents

    except Exception as e:
        return f'Error: {str(e)}\n'

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the content of a file, constrained to the working directory. Returns the first MAX_CHARS characters of the file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "working_directory": types.Schema(
                type=types.Type.STRING,
                description="The working directory.",
            ),
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to read, relative to the working directory.",
            ),
        },
    ),
)