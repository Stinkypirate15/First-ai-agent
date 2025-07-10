import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)#initializes client with API key for future requests
 
messages = [
    types.Content(role="user", parts=[types.Part(text=sys.argv[1])]),

    ]
try:
    #checks to see if there is a prompt
    response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=messages,
)   
  # attempts to generate a response; will fail if no prompt is provided
except IndexError as e:
    print(f"please enter a prompt ")
    sys.exit(1)

#checking for a verbose flag
if "--verbose" in sys.argv:
    
    #includes entire response including tokens and user prompt
    print(f"User prompt: {sys.argv[1]}")
    print(f"Model response: {response.candidates[0].content.parts[0].text}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
else:
    
    #only responds with LLM response 
    print(f"Model response: {response.candidates[0].content.parts[0].text}")
    







