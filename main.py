
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
    {'role': 'system', 'content': 
        '''
        you need to guess which person the user thinking
        you can ask the user some question to get more information about the person,
        but you can only ask 20 question, after that you need to guess the person, 
        if you guess wrong, you will lose, if you guess right, you will win
        
        Ask focused questions before you know the answer for sure, then try to guess.
        
        Yes or no question.
        '''
        
        },
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
    
    
