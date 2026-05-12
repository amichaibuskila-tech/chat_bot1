
from multiprocessing import context
from sqlite3 import Row

from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import UserMessage
from azure.core.credentials import AzureKeyCredential
import os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("GITHUB_TOKEN")

client = ChatCompletionsClient(
    endpoint="https://models.inference.ai.azure.com",
    credential=AzureKeyCredential(token),
)

def get_completion_from_messages(messages, model="gpt-4o-mini", temperature=0):
    response = client.complete(
        model=model,
        messages=messages,
        temperature=temperature, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message.content

context = [
    {'role': 'system', 'content': 'you are a helpful assistant.'},
]

def run_chat():
    print("To exit the chat, type 'quit' or 'exit'.")
    print("-" * 30)

    while True:
        prompt = input("User: ")        
        if prompt.lower() in ['quit', 'exit']:
            print("Goodbye!")
            break
        
        context.append({'role': 'user', 'content': prompt})
        
        response = get_completion_from_messages(context)
            
        context.append({'role': 'assistant', 'content': response})   
             
        print(f"Assistant: {response}")
        print("-" * 30)
            
if __name__ == "__main__":
    run_chat()