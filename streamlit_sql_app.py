import streamlit as st
#changing the model and indexing the content for vector store
from llama_index.llms import OpenAI
llm = OpenAI(temperature=0, model="gpt-4-1106-preview")
from llama_index import ServiceContext
service_context = ServiceContext.from_defaults(llm=llm)
from llama_index.indices.struct_store.sql_query import NLSQLTableQueryEngine
from llama_index import SQLDatabase
#importing SQLAlchemy and adding the db

from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    String,
    Integer,
    select,
    column,
    text,
    inspect,
    sql
)

from llama_index import Prompt

# Define a custom prompt
template = (
    "We want to query our sqlite database with following schrma. \n"
    "---------------------\n"
    "Column Name: date Data Type: DATETIME Nullable: NO Primary Key: NO \n"
    "Column Name: header Data Type: TEXT Nullable: NO Primary Key: NO \n"
    "Column Name: tags Data Type: TEXT Nullable: NO Primary Key: NO \n"
    "Column Name: article Data Type: TEXT Nullable: NO Primary Key: NO"
    "\n---------------------\n"
    "Given this information, please answer the question : {query_str} ,according to database query\n"
)
qa_template = Prompt(template)


# Create an engine that connects to an existing SQLite database
engine = create_engine('sqlite:///mining_articles1.db', future=True)


# Build query for SQL
sql_database = SQLDatabase(engine, include_tables=["articles_metals"])
query_engine = NLSQLTableQueryEngine(sql_database=sql_database, service_context=service_context, tables=["articles_metals"], text_to_sql_prompt=qa_template)

# Streamlit interface
st.title('You can ask here any question related to batery metals, batteries and EV')

# Check for the session state key, initialize if not present
if 'history' not in st.session_state:
    st.session_state.history = []

# User input
prompt = st.text_input("Ask here about batteries:", key="query_input", value="")

# Use a separate key for the submit button to avoid conflicts
submit_button = st.button('Submit Query', key='submit')

if submit_button and prompt:
    # Execute the query and store response
    response = query_engine.query(prompt).response
    xxx=query_engine.query(prompt).metadata
    st.session_state.history.append({"Query": prompt, "Response": response})
    print(xxx)

# Display conversation history
st.subheader("Conversation History:")
for interaction in st.session_state.history:
    st.text(f"Q: {interaction['Query']}")
    st.markdown(f"A: {interaction['Response']}")




