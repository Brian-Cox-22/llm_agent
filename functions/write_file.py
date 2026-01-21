from google.genai import types

schema_write_file = schema_run_python_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes the provided content to the file at the provided path",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to a file. Creates it if it does not exist",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="A string to be written to the file."
            )
        },
    ),
)

def write_file(working_directory, file_path, content):
    '''
    Adds the ability to write (or overwrite) to a file, so long
    as the file is within the scope specified by 'working_directory'
    '''
    import os

    try:

        # check that file is in working path
        working_path = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_path, file_path))
        valid_target_file = os.path.commonpath([working_path, target_file]) == working_path
        if not valid_target_file:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
        # check to see if file_path is a directory
        if os.path.isdir(target_file):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
    
        # make any missing dirs (not sure why this part is important yet)
        os.makedirs(os.path.dirname(target_file), exist_ok=True)
    

        # open and write:
        with open(target_file, 'w') as file:
            file.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error writing to file: {e}"