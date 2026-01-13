import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types

# set up
# source .venv/bin/activate
def get_api_key():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError('API Key is not present')
    return api_key

def track_tokens(response):
    usage = getattr(response, "usage_metadata", None)
    if not usage:
        raise RuntimeError("Failed API request")
    
    prompt_tokens = usage.prompt_token_count
    response_tokens = usage.total_token_count - prompt_tokens

    print(f"Prompt tokens: {prompt_tokens}\nResponse tokens: {response_tokens}")


def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="Prompt to chatbot")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

    args  = parser.parse_args()

    # messages replaces prompt, allows for multiple prompts
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    
    api_key = get_api_key()
    
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
    model='gemini-2.5-flash', 
    contents= messages
    )
    
    if args.verbose:
        print(f"User prompt: {messages}")
        track_tokens(response)
        print("Response:")
   
    print (response.text)

if __name__ == "__main__":
    main()
