import streamlit as st
import pandas as pd
import test_sql,re
from prompt import SYSTEM_MESSAGE
from azure_openai import get_completion
import json

# ngrok
# from ngrok import ngrok_url
# ngrok_url()
# main file
#  wget -q -O - ivpv4.icanhazip.com

def query_database(query, conn):
    """ Run SQL query and return results in a dataframe """
    return pd.read_sql_query(query, conn)


def get_query_dict_from_response(response):
    """
    This method extracts the query from the response from the
    openai.
    """
    # print('inside dict=====>:',response)
    # print('inside dict type of response ==>:',type(response))
    if type(response) == str:
        brack_count = response.count('{')
        brack_two_count = response.count('}')
        if brack_count == brack_two_count == 1:
            start_index = response.index('{')
            end_index = response.index('}') + 1
            return response[start_index:end_index]
    return response


# Schema Representation for table
schemas, tables = test_sql.get_table_schema()
print('schemas:',schemas,'and tables:',tables)
st.set_page_config(page_title="OpenAI With SQL", page_icon=":bar_chart:", layout="wide")
st.title("OpenAI search on SQL Database")
st.write("Ask anything about data in SQL database")
# Input field for the user to type a message

user_message = st.text_input("Enter your question:")

if user_message:
    
    # Format the system message with the schema
    formatted_system_message = SYSTEM_MESSAGE.format(schema_1=schemas, table_1=tables)
    # print('format:',formatted_system_message)
    response = get_completion(formatted_system_message, user_message)
    print('response:',response)
    try:
        if 'JSON' in response:
            dict_response = get_query_dict_from_response(response)
            # print('anser from the def of dict response:',dict_response)
            
            json_response = json.loads(dict_response)
            
            query = json_response['query']
        elif "I'm sorry" in response:
            print('no query getting')
        else:
            sql_query_pattern = re.compile(r'\bSELECT\b.*?;', re.DOTALL | re.IGNORECASE)
            match = sql_query_pattern.search(response)
            print('query group:',match.group())
            print('query normal:',match)
            query = match.group()
        # # Display the generated SQL query
        st.write("SQL Query:")
        st.code(query, language="sql")
    except Exception:
        st.write("""I'm sorry, but as an AI language model, please provide the more information !!!""")

    try:
        # Run the SQL query and display the results
        conn = test_sql.get_db_connection()
        sql_results = query_database(query, conn)
        st.write("Query Results:")
        st.dataframe(sql_results)

    except Exception:
        # st.write(f"An error occurred: {e}")
        st.write("""I'm sorry, but as an AI language model, please provide the more information !!!""")