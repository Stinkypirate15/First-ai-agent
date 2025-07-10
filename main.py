import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
 
messages = [
    types.Content(role="user", parts=[types.Part(text=sys.argv[1])]),

    ]
try:
    
    response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=messages,
)   
  
except IndexError as e:
    print(f"please enter a prompt ")
    sys.exit(1)


if "--verbose" in sys.argv:
    
    
    print(f"User prompt: {sys.argv[1]}")
    print(f"Model response: {response.candidates[0].content.parts[0].text}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
else:
    
    
    print(f"Model response: {response.candidates[0].content.parts[0].text}")
    




# After you get your response from generate_content()



