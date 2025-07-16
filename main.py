import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import *

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
system_prompt ="""
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

# Check if prompt is provided BEFORE using it
try:
    user_prompt = sys.argv[1]
except IndexError:
    print("please enter a prompt")
    sys.exit(1)

messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]

response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=messages,
    config=types.GenerateContentConfig(
    tools=[available_functions], system_instruction=system_prompt
),
)

# Rest of your code for handling verbose flag and printing...

#checking for a verbose flag
candidate = response.candidates[0]
function_calls = getattr(candidate, "function_calls", None)

#checking for a verbose flag
candidate = response.candidates[0]

# Check if there are function calls in the parts
if candidate.content.parts:
    for part in candidate.content.parts:
        if hasattr(part, 'function_call') and part.function_call:
            function_call = part.function_call
            # Call your dispatcher, passing the verbose flag (True if '--verbose' in sys.argv else False)
            verbose = "--verbose" in sys.argv
            function_call_result = call_function(function_call, verbose=verbose)
            # In verbose mode, your function already prints the result
            # In non-verbose mode, print just the result
            if not verbose:
                print(function_call_result.parts[0].function_response.response["result"])
        elif hasattr(part, 'text') and part.text:
            print(part.text)

if "--verbose" in sys.argv:
    print(f"User prompt: {user_prompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    







