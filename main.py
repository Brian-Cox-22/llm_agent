import os
import argparse
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function

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

def call_llm(messages, verbose):
    api_key = get_api_key()
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable not set")

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
            model='gemini-2.5-flash', 
            contents= messages,
            config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)
            )
    
    if not response.usage_metadata:
        raise RuntimeError("Gemini API response appears to be malformed")

    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)
    

    if response.candidates:
        for candidate in response.candidates:
            if candidate.content:
                messages.append(candidate.content)
    
    # if no function calls, we're done
    if not response.function_calls:
        return response.text
    

    function_responses = []
    for function_call in response.function_calls:
        result = call_function(function_call, verbose)
        if (
            not result.parts
            or not result.parts[0].function_response
            or not result.parts[0].function_response.response
        ):
            raise RuntimeError(f"Empty function response for {function_call.name}")
        if verbose:
            print(f"-> {result.parts[0].function_response.response}")
        function_responses.append(result.parts[0])


    # feed function response back to LLM
    messages.append(types.Content(role="user", parts=function_responses))


def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="Prompt to chatbot")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args  = parser.parse_args()

    # messages replaces prompt, allows for multiple prompts
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    
    if args.verbose:
        print(f"User prompt: {args.user_prompt}\n")

    
    # now we loop
    for i in range(20):
        response = call_llm(messages, args.verbose)
        if response:
            print("Final response:")
            print(response)
            return
    
    print("Error: Agent failed to reach a conclusion")
    sys.exit(1)
    
    


    # else:
    #     print (response.text)
    

if __name__ == "__main__":
    main()
