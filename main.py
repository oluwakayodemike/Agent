import os
import argparse
from dotenv import load_dotenv
from openai import OpenAI

def main():
    print("Hello from Agent Smith!")
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
    args = parser.parse_args()
    
    messages = [
        {
            "role": "user",
            "content": args.user_prompt,
        }
    ]
    
    response = client.chat.completions.create(model="openrouter/free", messages=messages)

    message_dict = messages[0]
    print(f"User prompt: {message_dict.get('content')}")

    if response is None:
        raise RuntimeError("No response generated ")
        
    print(f"Prompt tokens: {response.usage.prompt_tokens}")
    print(f"Response tokens: {response.usage.completion_tokens}")
    print(f"Response: {response.choices[0].message.content}")
    
if __name__ == "__main__":
    main()
