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

    i = 0

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    while i <= 20:
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=messages,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    tools=[available_functions],
                ),
            )
        except Exception as e:
            print(f"Error: {e}")
            continue

        # Check if we're done - no function calls and we got a text response
        if not response.function_calls and response.text:
            print(response.text)
            break

        # Append the model's response to our message history
        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)

        # Handle function calls - execute each one and collect results
        if response.function_calls:
            function_parts = []
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

                    # Build Part from function response to send back to the model
                    function_parts.append(
                        types.Part.from_function_response(
                            name=function_call.name,
                            response=result_response,
                        )
                    )

                except Exception as e:
                    print(f"Error: {e}")

            # Send all function results back as one message
            if function_parts:
                messages.append(types.Content(role="user", parts=function_parts))

        i += 1    
    
if __name__ == "__main__":
    main()
