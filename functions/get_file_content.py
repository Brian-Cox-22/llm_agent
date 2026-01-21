from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Opens a file at a designated file path and returns the contents as a string. Currently trunkates at 10000 chars",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to a python file",
            )
            ,
        },
    ),
)


'''
Returns the information in a file as a string or an error message
'''
def get_file_content(working_directory, file_path):
    import os
    from config import MAX_CHARS

    # check that file is in working path
    working_path = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_path, file_path))
    valid_target_file = os.path.commonpath([working_path, target_file]) == working_path
    if not valid_target_file:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    # check if it's a file
    if not os.path.isfile(target_file):
        return f'Error: File not found or is not a regular file: "{file_path}"'



    # read the file (first 10000 char(MAX_CHAR)) and list contents as string
    try:
        with open(target_file, 'r') as file:
            file_content_string = file.read(MAX_CHARS)

        # checks to see if the file was larger
            if file.read(1):
                file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            
            return file_content_string

    except:
        return f"Error: Unable to open {file_path}"
