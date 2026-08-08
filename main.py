import os
import argparse
import json
from prompts import system_prompt
from call_function import available_functions, call_function
from dotenv import load_dotenv
from openai import OpenAI

def main():
    # print("Hello from Agent Smith!")
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    
    if api_key is None:
        raise RuntimeError("API key not found")
    
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
        
    messages = [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": args.user_prompt
        }
    ]
    
    if args.verbose:
        print(f"User prompt: {args.user_prompt}\n")
        
    response = client.chat.completions.create(model="openrouter/free", messages=messages, tools=available_functions, temperature=0,)
    
    if response is None:
        raise RuntimeError("No response generated ")
        
    if response.usage and args.verbose:
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")

    message = response.choices[0].message
    
    if not message.tool_calls:
        if message.content:
            print(f"Response: {response.choices[0].message.content}")
        
    if message.tool_calls:    
        for tool_call in message.tool_calls:
            result_message = call_function(tool_call, args.verbose)

            if not result_message["content"]:
                raise Exception("content missing")

            if args.verbose:
                print(f"-> {result_message['content']}")
if __name__ == "__main__":
    main()
