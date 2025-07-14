from functions.get_files_info import run_python_file

# Now call your function with required test arguments and print results


print(run_python_file("calculator", "main.py"))
print(run_python_file("calculator", "tests.py"))
print(run_python_file("calculator", "../main.py"))
print(run_python_file("calculator", "nonexistent.py"))
