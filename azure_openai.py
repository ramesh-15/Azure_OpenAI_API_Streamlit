from dotenv import load_dotenv
import openai
import os

# Set your Azure API key
# client = AzureOpenAI(
#     # https://learn.microsoft.com/en-us/azure/ai-services/openai/reference#rest-api-versioning
#     api_version="2023-07-01-preview",
#     # https://learn.microsoft.com/en-us/azure/cognitive-services/openai/how-to/create-resource?pivots=web-portal#create-a-resource
#     azure_endpoint="https://ahex-ai.openai.azure.com",
#     azure_ad_token="e61550e0-4ac5-4a37-baee-83d18c04dfea",
#     # azure_ad_token_provider=DefaultAzureCredential(),
#     azure_ad_token_provider='9f56e29c-24cc-4304-b8a2-9a3f61de201e',
# )

#openai


load_dotenv()


openai.api_type = "azure"
openai.api_version = "2023-05-15" 
openai.api_key = "996d1769a4b14d96bd2ba7ec07f650f9"
openai.api_base = "https://ahex-ai.openai.azure.com"
deployment_name='ahex-sqldb'

def get_completion(system_message, user_message, deployment_name='ahex-sqldb', temperature=0, max_tokens=500) -> str:
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








    
   
    
