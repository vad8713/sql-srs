## pylint: disable=missing-module-docstring
import io

import duckdb
import pandas as pd
import streamlit as st

con = duckdb.connect("Data/exercises_sql_tables.db", read_only=False)

st.write(
    """
SQL SRS
Space Repetition System SQL Practice
"""
)

with st.sidebar:

    theme = st.selectbox(
        "What would you like to review",
        ("Cross_joins", "GroupBy", "Windows Functions"),
        index=None,
        placeholder="Select a theme",
    )
    st.write("You selected" ,theme)

    exercise = con.execute(f"SELECT * FROM memory_state WHERE theme = '{theme}' ").df()
    st.write(exercise)

# ANSWER_STRING = """
# SELECT * FROM beverages
# CROSS JOIN food_items
# """
# solution_df = duckdb.sql(ANSWER_STRING).df()

st.header("Enter your code:")
sql_query = st.text_area(label="Enter an SQL request", key="user_input")
if sql_query:
    result = duckdb.sql(sql_query).df()
    st.dataframe(result)

#     if solution_df.shape[0] != result.shape[0]:
#         st.write(
#             f"Result has {solution_df.shape[0] - result.shape[0]} differences with the solution_df"
#         )
#
#     try:
#         # set datframes columns in the same order
#         result = result[solution_df.columns]
#         st.dataframe(result.compare(solution_df))
#     except KeyError as e:
#         st.write("Some columns are missing")
#
# tab2, tab3 = st.tabs(["Tables", "Solution"])
# with tab2:
#     st.write("Table beverages")
#     st.dataframe(beverages)
#     st.write("Table food_items")
#     st.dataframe(food_items)
#     st.write("Expected")
#     st.dataframe(solution_df)
#
# with tab3:
#     st.write(ANSWER_STRING)
