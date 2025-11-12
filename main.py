import os
import argparse
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import system_prompt
from call_function import available_funcs, call_function


def parse_args():
    parser = argparse.ArgumentParser(
        description="Fraude - Claude from Wish",
        epilog="Example: python main.py 'How do I build a calculator app?'",
    )
    parser.add_argument("prompt")
    parser.add_argument("--verbose", action="store_true", help="Show debug info")
    parser.add_argument("--working-dir", default="calculator", help="Working directory")
    args = parser.parse_args()
    return args


def create_client():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print(
            "Error: GEMINI_API_KEY not found in environment variables", file=sys.stderr
        )
        sys.exit(1)
    client = genai.Client(api_key=api_key)
    return client


def get_response(client, args):
    user_prompt = args.prompt

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    MAX_ITERATIONS = 20
    for iter in range(MAX_ITERATIONS):
        if args.verbose:
            print(f"\n---Iteration {iter + 1} ---")

        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_funcs], system_instruction=system_prompt
                ),
            )
            if args.verbose:
                print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
                print(
                    f"Response tokens: {response.usage_metadata.candidates_token_count}"
                )

            for candidate in response.candidates:
                messages.append(candidate.content)

            if not response.function_calls:
                if args.verbose:
                    print("\n--- Final Response ---")
                return response.text

            function_responses = []
            for function_call_part in response.function_calls:
                function_call_result = call_function(function_call_part, args.verbose)

                if args.verbose:
                    print(
                        f"-> {function_call_result.parts[0].function_response.response}"
                    )

                function_responses.append(function_call_result.parts[0])

            if not function_responses:
                raise Exception("No function responses generated")

            messages.append(types.Content(role="user", parts=function_responses))

        except Exception as e:
            print(f"Error during iteration {iter + 1}: {e}", file=sys.stderr)
            sys.exit(1)
    print(f"Warning: Reached maximum iterations ({MAX_ITERATIONS})", file=sys.stderr)
    return "Error: Maximum iterations reached"


def main():
    args = parse_args()
    client = create_client()
    if args.verbose:
        print(f"User Prompt: {args.prompt}\n")

    final_response = get_response(client, args)
    print(final_response)


if __name__ == "__main__":
    main()
