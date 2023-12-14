from dotenv import load_dotenv
import openai
import os


load_dotenv()

#  azure connection
openai.api_type = "azure"
openai.api_version = "2023-05-15" 
openai.api_key = "996d1769a4b14d96bd2ba7ec07f650f9"
openai.api_base = "https://ahex-ai.openai.azure.com"
deployment_name='ahex-sqldb'

# Set OpenAI API credentials and configuration new azure openai connectin
# openai.api_type = "azure"
# openai.api_version = "2023-05-15"
# openai.api_key = "03f671cca3574127a43b8db73c7f7b57"
# openai.api_base = "https://azure-openai-sql-services.openai.azure.com/"
# deployment_name = 'deploy_azure_sql_db'



def get_completion(system_message, user_message, deployment_name='ahex-sqldb', temperature=0, max_tokens=1000) -> str:
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











    
   
    
