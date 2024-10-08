from cProfile import label

import streamlit as st
import pandas as pd
import duckdb
from pyarrow import table

st.write("""
SQL SRS
Space Repetition System SQL Practice
""")

option = st.selectbox(
    "What would you like to review",
    ('Joins', 'GroupBy','Windows Functions'),
    Index=None,
    placeholder="Select a theme"
)

st.write("You selected: ",option)

data = {"a":[1,2,3], "b":[4, 5, 6]}
df = pd.DataFrame(data)

tab1,tab2,tab3 = st.tabs(["Cat","Dogs","Owl"])

with tab1:
    #default_query = "SELECT * FROM df"
    sql_query = st.text_input(label='Enter an SQL request')
    result = duckdb.sql(sql_query).df()
    st.write('Proceeding Dataframe')
    st.dataframe(result)

with tab2:
    st.header("A Dog")
    st.image("https://static.streamlit.io/examples/dog.jpg",width=200)

with tab3:
    st.header("A Owl")
    st.image("https://static.streamlit.io/examples/owl.jpg",width=200)

