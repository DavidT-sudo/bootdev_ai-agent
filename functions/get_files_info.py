import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    abs_working_directory = os.path.abspath(working_directory)
    abs_target_dir = os.path.abspath(os.path.join(working_directory, directory))
    
    # Will be True or False
    valid_target_dir = os.path.commonpath([abs_working_directory, abs_target_dir]) == abs_working_directory

    if not valid_target_dir:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.exists(abs_target_dir):
        return f'Error: "{directory}" is not a directory'

    files_info = ""

    try:
        for entry in os.scandir(abs_target_dir):
            files_info += f"- {entry.name}: file_size={entry.stat().st_size}, is_dir={entry.is_dir()}\n"
    except Exception as e:
        return f'Error: {str(e)}'
    
    return f"Result for {os.path.basename(abs_target_dir)} directory:\n{files_info}"
            

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)