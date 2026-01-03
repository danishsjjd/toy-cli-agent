import argparse
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.call_function import available_functions, call_function
from prompts import system_prompt

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

parser = argparse.ArgumentParser(description="Toy CLI agent")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

config = types.GenerateContentConfig(
    tools=[available_functions], system_instruction=system_prompt
)

messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]


def main():
    response = client.models.generate_content(
        model="gemini-2.5-flash", contents=messages, config=config
    )

    if response.usage_metadata is None:
        raise RuntimeError("Api error")

    if response.candidates is not None:
        for candidate in response.candidates:
            if candidate.content:
                messages.append(candidate.content)

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    if response.function_calls and len(response.function_calls) > 0:
        for function_call in response.function_calls:
            call_function_result = call_function(function_call, args.verbose)

            messages.append(
                types.Content(role="user", parts=call_function_result.parts)
            )

            if call_function_result.parts is None:
                raise Exception("")
            function_response = call_function_result.parts[0].function_response

            if function_response is None:
                raise Exception("")

            response = function_response.response

            if args.verbose:
                print(f"-> {response}")

    else:
        print(response.text)
        return True


for _ in range(20):
    if main():
        break
