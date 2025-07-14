from functions.get_files_info import get_file_content

# Now call your function with required test arguments and print results

print(get_file_content("calculator", "main.py"))
print( get_file_content("calculator", "pkg/calculator.py"))
print(get_file_content("calculator", "/bin/cat"))