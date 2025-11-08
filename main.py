import os
import argparse
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types


def parse_args():
    parser = argparse.ArgumentParser(
        description="Fraude - Claude from Wish",
        epilog="Example: python main.py 'How do I build a calcultor app?'",
    )
    parser.add_argument("prompt")
    parser.add_argument("--verbose", action="store_true", help="Show debug info")

    args = parser.parse_args()
    return args


def create_client():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    return client


def get_response(client, args):
    user_prompt = args.prompt

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
    )

    return response


def log_debug(args, response):
    user_prompt = args.prompt
    if args.verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


def main():
    args = parse_args()
    client = create_client()
    response = get_response(client, args)
    log_debug(args, response)
    print("Response:")
    print(response.text)


if __name__ == "__main__":
    main()
