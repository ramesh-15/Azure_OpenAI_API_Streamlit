from dotenv import load_dotenv
import openai
import os


load_dotenv()

#  azure connection
openai.api_type = "azure"
openai.api_version = "2023-05-15" 
openai.api_key = "open_api_key"
openai.api_base = "endpoint"
deployment_name='deployment_name'





def get_completion(system_message, user_message, deployment_name='deployment_name', temperature=0, max_tokens=1000) -> str:
    """
    This method calls openai chatcompletion with the provided system message
    and user message(passed by user) and returns the content response returned 
    by openai model.
    """
    messages = [
        {'role': 'system', 'content': system_message},
        {'role': 'user', 'content': f"{user_message}"}
    ]
    
    response = openai.ChatCompletion.create(
        engine=deployment_name,
        messages=messages,
        temperature=temperature, 
        max_tokens=max_tokens, 
    )
    
    return response.choices[0].message["content"]











    
   
    
