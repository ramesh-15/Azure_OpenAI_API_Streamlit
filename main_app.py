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
    print('inside the dict res:',response)
    return response


# Schema Representation for table
schemas, tables = test_sql.get_table_schema()
# print('schemas:',schemas,'and tables:',tables)
st.set_page_config(page_title="OpenAI With SQL", page_icon=":bar_chart:", layout="wide")
st.title("OpenAI search on SQL Database")
st.write("Ask anything about data in SQL database")
# Input field for the user to type a message
# options = ["Upload", "Excel", "CSV", "Data Source"]

# st.set_page_config(menu_items=dict(
#     label="Select Data Source",
#     icon="download",
#     click=st.selectbox,
#     args=(options,),
   
# ))


def upload_file():
    uploaded_file = st.file_uploader("Choose a file", type=["csv", "xlsx"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file, engine='openpyxl')
        st.write('file uploded successfully')
        st.dataframe(df)
        return df
# Create the dropdown using st.selectbox
selected_option = st.sidebar.selectbox("Select functionality", ["Upload","File Upload",  "Data Source"])

# Perform action based on selected option
if selected_option == "File Upload":
    st.header("Upload File")
    df_res =upload_file()
    if df_res is not None:
        input_query=st.text_input("Enter your question:")
        result_df = df_res.query(input_query)
        print("process data:",result_df)
        st.write(result_df)
elif selected_option == 'Data Source':
    st.header('upload your data source')
else:
    user_message = st.text_input("Enter your question:")

        
    if user_message:
        
        # Format the system message with the schema
        formatted_system_message = SYSTEM_MESSAGE.format(schema_1=schemas, table_1=tables)
        print('format:',formatted_system_message)
        response = get_completion(formatted_system_message, user_message)
        print('response:',response)
        try:
            print('in json')
            dict_response = get_query_dict_from_response(response)
            # print('anser from the def of dict response:',dict_response)
            print('dict:',dict_response)
            json_response = json.loads(dict_response)
            
            query = json_response['query']
            error = json_response['error']
            # elif "I'm sorry" in response:
            #     print('no query getting, provide more information !!!')
            # else:
            #     sql_query_pattern = re.compile(r'\bSELECT\b.*?;', re.DOTALL | re.IGNORECASE)
            #     match = sql_query_pattern.search(response)
            #     # print('query group:',match.group())
            #     # print('query normal:',match)
            #     query = match.group()
            # # Display the generated SQL query
            if query is None:
                st.write(error)
            else:
                st.write("SQL Query:")
                st.code(query, language="sql")

                # Run the SQL query and display the results
                conn = test_sql.get_db_connection()
                sql_results = query_database(query, conn)
                st.write("Query Results:")
                st.dataframe(sql_results)
        

        except Exception as e:
        #     # st.write(f"An error occurred: {e}")
            st.write(response)


    
        
