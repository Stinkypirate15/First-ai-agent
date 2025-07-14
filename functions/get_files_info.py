import os

def get_files_info(working_directory, directory=None):
 
    results = []
    abs_root = os.path.abspath(working_directory)
    if directory is None:
        abs_target = abs_root
    else:
        abs_target = os.path.abspath(os.path.join(working_directory, directory))

    if not abs_target.startswith(abs_root):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(abs_target):
        return f'Error: "{directory}" is not a directory'

    for entry in os.listdir(abs_target):
        full_path = os.path.join(abs_target, entry)
        size = os.path.getsize(full_path)
        is_dir = os.path.isdir(full_path)
        results.append(f"- {entry}: file_size={size} bytes, is_dir={is_dir}")

    return "\n".join(results)
            

def get_file_content(working_directory, file_path):
    max_chars= 10000
    abs_file_path = os.path.abspath(os.path.join(working_directory,file_path))
    abs_working_directory = os.path.abspath(working_directory)
    try:
        if not abs_file_path.startswith(abs_working_directory):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
            

        if not os.path.isfile(abs_file_path): 
            return f'Error: File not found or is not a regular file: "{file_path}"'
        else: 
            with open(abs_file_path,"r") as f:
                file_content_string = f.read()
                if len(file_content_string) > max_chars:
                    trunc_characters= file_content_string[:10000]
                    file_name = f'[...File "{file_path}" truncated at 10000 characters]'
                    appended_File=trunc_characters + file_name
    
                    return appended_File
                else:
                    return file_content_string
        
    except Exception as e:
        return f"Error {e}"
        
def write_file(working_directory, file_path, content):
    abs_file_path = os.path.abspath(os.path.join(working_directory,file_path))
    abs_root = os.path.abspath(working_directory)
    if not abs_file_path.startswith(abs_working_directory):