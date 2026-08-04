import os
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
    
    messages = [
        {
            "role": "user",
            "content": "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.",
        }
    ]
    
    response = client.chat.completions.create(model="openrouter/free", messages=messages)
    
    print(response.choices[0].message.content)

if __name__ == "__main__":
    main()
