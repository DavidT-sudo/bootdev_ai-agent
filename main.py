import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if(api_key is None):
    raise ValueError("GEMINI_API_KEY is not set")

client = genai.Client(api_key=api_key)

def main():
    print("Hello from bookbot!")
    response = client.models.generate_content(model="gemini-2.5-flash", contents="Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.")
    
    print("Prompt tokens:", response.usage_metadata.prompt_token_count)
    print("Response tokens:", response.usage_metadata.candidates_token_count)


    print(response.text)

if __name__ == "__main__":
    main()
