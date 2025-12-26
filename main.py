import os
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if(api_key is None):
    raise ValueError("GEMINI_API_KEY is not set")

client = genai.Client(api_key=api_key)

def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

    args = parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    
    response = client.models.generate_content(model="gemini-2.5-flash", contents=messages,
        config=types.GenerateContentConfig(system_instruction=system_prompt,
        tools=[available_functions])
    )
    
    if not response.function_calls:
        print(response.text)
    else:
        for function_call in response.function_calls:
            try:
                function_result = call_function(function_call, args.verbose)
                result_response = function_result.parts[0].function_response.response
                
                if not result_response:
                    print(f"Error: Function '{function_call.name}' returned no result")
                    continue
                
                if args.verbose:
                    print(f"-> {result_response}")
                else:
                    print(result_response.get("result", result_response))
                    
            except Exception as e:
                print(f"Error: {e}")
            
    
    
    
if __name__ == "__main__":
    main()
