from google.genai import types
from config import WORKING_DIR
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.run_python_file import schema_run_python_file, run_python_file
from functions.write_file import schema_write_file, write_file
from functions.get_file_content import schema_get_file_content, get_file_content

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info, 
        schema_run_python_file, 
        schema_write_file, 
        schema_get_file_content
        ]
)


function_map = {
    "get_file_content": get_file_content,
    "get_files_info": get_files_info,
    "run_python_file": run_python_file,
    "write_file": write_file
    }

def call_function(function_call, verbose=False):
    '''
    Docstring for call_function
    
    :param function_call: types.FunctionCall object that has:
        name(name of function, a string)
        args(dict of named arguments to the function)
    :param verbose: if specified, print function name and args, otherwise, just prints name
    '''
    if verbose:
        print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print(f" - Calling function: {function_call.name}")
    

    function_name = function_call.name or ""

    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    args = dict(function_call.args) if function_call.args else {}

    args["working_directory"] = WORKING_DIR

    # should always be a string
    function_result = function_map[function_name](**args)

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )

