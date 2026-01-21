from google.genai import types


# have to fix the types on this still :/
# Maybe fixed it now? Not sure if I need to somehow set up a subtype for the args type
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Check if a file is a viable python file; if so runs it as a subprocess",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to a python file",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items = types.Schema(
                    type = types.Type.STRING,
                ),
                description="Any additional arguments that the python function needs. Default is none."
                )
            }
        ),
    )

def run_python_file(working_directory, file_path, args=None):
    import os
    import subprocess
    
    try:
        working_path = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_path, file_path))
        valid_target_file = os.path.commonpath([working_path, target_file]) == working_path
        if not valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not target_file.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'
        
        # setting up a sub process
        command = ["python", target_file]
        if args:
            command.extend(args)
        
        # print('Command list:', repr(command))

        # need to check if this is settingworking directory
        ran_command = subprocess.run(command, text=True, capture_output=True, timeout=30)
        # print(ran_command)

        if ran_command.returncode == 0:
            if not ran_command.stdout and not ran_command.stderr:
                return "No outcome produced"
            return f"STDOUT: {ran_command.stdout} \nSTDERR: {ran_command.stderr}"
        
        else:
            return f"Process exited with code {ran_command.returncode}"
        
    except Exception as e:
        return f"Error: {e}"
