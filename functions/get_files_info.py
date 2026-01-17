'''
takes directory and returns a string
'''
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)

def get_files_info(working_directory, directory="."):
    import os
    
    '''
   Directory treated as local path within working_directory
   Used to limit scope of what LLM can see
    '''
    
    working_path = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_path, directory))
    valid_target_dir = os.path.commonpath([working_path, target_dir]) == working_path


    if not valid_target_dir:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    # check if is a directory that exhists
    if not os.path.isdir(target_dir):
        return f'Error: "{directory}" is not a directory'


    
    # directory_as_list = target_dir[1:].split('/')
    string_list = []
    for item in os.listdir(target_dir):
        full_path = os.path.join(target_dir, item)
        
        try:
            size = os.path.getsize(full_path)
        except:
            return f"Error: could not get {item} size"
        
        try:
            is_dir = os.path.isdir(full_path)
        except:
            return f"Error: could not check if {item} is a directory"
        
        string = f"- {item}: file_size={size} bytes, is_dir={is_dir}"
        string_list.append(string)
    return "\n".join(string_list)

