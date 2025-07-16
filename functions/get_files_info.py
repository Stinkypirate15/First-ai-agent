import os
import subprocess
from google.genai import types

def get_files_info(working_directory, directory=None):

    results = []
    abs_root = os.path.abspath(working_directory)
    
    # If no specific directory requested, list the root working directory
    if directory is None:
        abs_target = abs_root
    else:
        # Create absolute path for the requested subdirectory
        abs_target = os.path.abspath(os.path.join(working_directory, directory))

    # Security check: prevent directory traversal attacks
    if not abs_target.startswith(abs_root):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    # Validate that the target is actually a directory
    if not os.path.isdir(abs_target):
        return f'Error: "{directory}" is not a directory'

    # Iterate through directory contents and gather file information
    for entry in os.listdir(abs_target):
        full_path = os.path.join(abs_target, entry)
        size = os.path.getsize(full_path)
        is_dir = os.path.isdir(full_path)
        results.append(f"- {entry}: file_size={size} bytes, is_dir={is_dir}")

    return "\n".join(results)

def get_file_content(working_directory, file_path):
    """
    Reads and returns the content of a file within the working directory.
    
    Args:
        working_directory: The base directory to operate within
        file_path: Path to the file (relative to working_directory)
    
    Returns:
        File content as string, or error message if file cannot be read
    """
    max_chars = 10000  # Limit to prevent memory issues with large files
    
    # Create absolute paths for security validation
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    abs_working_directory = os.path.abspath(working_directory)
    
    try:
        # Security check: ensure file is within permitted directory
        if not abs_file_path.startswith(abs_working_directory):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        # Validate file exists and is a regular file
        if not os.path.isfile(abs_file_path): 
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        # Read file content
        with open(abs_file_path, "r") as f:
            file_content_string = f.read()
            
            # Truncate if file is too large to prevent memory issues
            if len(file_content_string) > max_chars:
                truncated_content = file_content_string[:max_chars]
                truncation_notice = f'[...File "{file_path}" truncated at {max_chars} characters]'
                return truncated_content + truncation_notice
            else:
                return file_content_string
        
    except Exception as e:
        return f"Error {e}"

def write_file(working_directory, file_path, content):
    """
    Writes content to a file within the working directory.
    
    Args:
        working_directory: The base directory to operate within
        file_path: Path where to write the file (relative to working_directory)
        content: String content to write to the file
    
    Returns:
        Success message or error message
    """
    # Create absolute paths for security validation
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    abs_root = os.path.abspath(working_directory)
    
    # Security check: prevent writing outside permitted directory
    if not abs_file_path.startswith(abs_root):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    # Create parent directories if they don't exist
    os.makedirs(os.path.dirname(abs_file_path), exist_ok=True)
    
    # Write content to file
    with open(abs_file_path, "w") as f:
        f.write(content)
   
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

def run_python_file(working_directory, file_path):
    """
    Executes a Python file within the working directory with security constraints.
    
    Args:
        working_directory: The base directory to operate within
        file_path: Path to the Python file to execute (relative to working_directory)
    
    Returns:
        Formatted output containing stdout, stderr, and exit code information
    """
    # Create absolute paths to prevent directory traversal attacks
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    abs_root = os.path.abspath(working_directory)
    
    try:
        # Security check: ensure file is within working directory
        if not abs_file_path.startswith(abs_root):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        # Validate file exists
        if not os.path.isfile(abs_file_path): 
            return f'Error: File "{file_path}" not found.'
    
        # Validate it's a Python file
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'
        
        # Execute the Python file with security constraints
        # - 30 second timeout to prevent infinite execution
        # - Capture both stdout and stderr
        # - Run in the working directory context
        result = subprocess.run(['python', file_path], 
                              cwd=abs_root, 
                              capture_output=True, 
                              text=True, 
                              timeout=30)
        
        # Handle case where no output was produced
        if not result.stdout.strip() and not result.stderr.strip():
            return "No output produced."
        
        # Format output with proper prefixes
        output = f"STDOUT:{result.stdout}STDERR:{result.stderr}"
        
        # Include exit code information if process failed
        output = ""
        if result.stdout:
            output += result.stdout
        if result.stderr:
            output += result.stderr
        if result.returncode != 0:
            output += f"Process exited with code {result.returncode}"
        return output
        
    except Exception as e:
        # Catch any unexpected errors during execution
        return f"Error: executing Python file: {e}"



        result = functions[function_call_part.name](**args)
def call_function(function_call_part, verbose=False):
    # 1. If verbose is True, print the function being called and its arguments
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")

    # 2. Copy the arguments from the function call and add 'working_directory'
    args = function_call_part.args.copy()
    args["working_directory"] = "./calculator"

    # 3. Check if the function name exists in your dictionary of functions
    if function_call_part.name not in functions:
        # a. If not, return an error wrapped in the required structure
        function_call_result = types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )
    else:
        # b. If the function exists:
        #    i. Call the function using all arguments
        result = functions[function_call_part.name](**args)
        #    ii. Wrap the result in the required structure
        function_call_result = types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"result": result},
                )
            ],
        )

    # 4. If verbose, print the result after calling the function
    if verbose:
        # ONLY print the actual result string!
        print(function_call_result.parts[0].function_response.response["result"])

    # 5. Return the wrapped result or error
    return function_call_result



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
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="gets contents of files",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="list the contents of a file",
            ),
        },
    ),
)
functions = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "run_python_file": run_python_file,
    "write_file": write_file,
}
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="allows you to run the contents of a python file ",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Executes a Python file and returns the output",
            ),
        },
    ),
)
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="allows you to write to a file ",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path where to write the file",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write to the file",
            ),
        },
    ),
)
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_run_python_file,
        schema_write_file,
        schema_get_file_content
    ]
)




