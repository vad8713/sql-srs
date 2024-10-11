## pylint: disable=missing-module-docstring
import io

import duckdb
import pandas as pd
import streamlit as st

st.write(
    """
SQL SRS
Space Repetition System SQL Practice
"""
)

with st.sidebar:

    option = st.selectbox(
        "What would you like to review",
        ("Joins", "GroupBy", "Windows Functions"),
        index=None,
        placeholder="Select a theme",
    )

    st.write("You selected: ", option)

CSV = """
beverage,price
orange juice,2.5
Expresso,2
Tea,3
"""
beverages = pd.read_csv(io.StringIO(CSV))

CSV2 = """
food_item, food_price
cookie juice,2.5
bread with chocolate,2
muffin, 3
"""
food_items = pd.read_csv(io.StringIO(CSV2))

ANSWER_STRING = """
SELECT * FROM beverages
CROSS JOIN food_items 
"""

solution_df = duckdb.sql(ANSWER_STRING).df()
st.header("Enter your code:")
sql_query = st.text_area(label="Enter an SQL request", key="user_input")
if sql_query:
    result = duckdb.sql(sql_query).df()
    st.dataframe(result)

    if solution_df.shape[0] != result.shape[0]:
        st.write(
            f"Result has {solution_df.shape[0] - result.shape[0]} differences with the solution_df"
        )

    try:
        # set datframes columns in the same order
        result = result[solution_df.columns]
        st.dataframe(result.compare(solution_df))
    except KeyError as e:
        st.write("Some columns are missing")

tab2, tab3 = st.tabs(["Tables", "Solution"])
with tab2:
    st.write("Table beverages")
    st.dataframe(beverages)
    st.write("Table food_items")
    st.dataframe(food_items)
    st.write("Expected")
    st.dataframe(solution_df)

with tab3:
    st.write(ANSWER_STRING)
