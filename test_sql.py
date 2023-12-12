import mysql.connector

server_name = 'localhost'
database_name = 'sakila'
username = 'root'
password = 'root'
chunk_size = 10000

# sql connection

def get_db_connection():
    connection = mysql.connector.connect(host=server_name,
                                         database=database_name,
                                         user=username,
                                         password=password)
    return connection


def get_list_of_tables(cursor):
    """
    This function gets the list of tables available
    in the database connected to the mysql server
    and returns the same
    :param cursor:
    :return: list of tables
    """
    query = "show tables;"
    cursor.execute(query)
    tables = cursor.fetchall()
    table_list = []
    for each_table in tables:
        table_list.append(each_table[0])
    print(f"Number of tables fetched: {len(table_list)}")
    return table_list


def get_tables_db_schema(cursor, tables):
    db_schema = {}

    for table in tables:
        query = f"SHOW FULL COLUMNS FROM {database_name}.{table};"
        cursor.execute(query)
        columns = cursor.fetchall()

        column_details = {}
        for column in columns:
            column_name = column[0]
            column_description = column[-1]
            column_details[column_name] = column_description

        db_schema[table] = column_details
    return db_schema


def get_table_schema():
    connection = mysql.connector.connect(host=server_name,
                                         database=database_name,
                                         user=username,
                                         password=password)
    db_schema = {}
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor()
        list_of_tables = get_list_of_tables(cursor)
        db_schema = get_tables_db_schema(cursor, list_of_tables)

    connection.close()

    return db_schema, list_of_tables
