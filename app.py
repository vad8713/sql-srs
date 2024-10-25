## pylint: disable=missing-module-docstring
## pylint: disable=exec-used

import logging
import os

import duckdb

# import pandas as pd
import streamlit as st

if "Data" not in os.listdir():
    logging.error(os.listdir())
    logging.error("Creating Data folder")
    os.mkdir("Data")

if "exercises_sql_tables.db" not in os.listdir("Data"):
    ## pylint: disable-next=consider-using-with
    exec(open("init_db.py", encoding="utf-8").read())

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

    if theme:
        st.write("You selected", theme)
        select_theme_string = f"SELECT * FROM memory_state WHERE theme = '{theme}'"
    else:
        select_theme_string = "SELECT * FROM memory_state"

    exercise = (
        con.execute(select_theme_string)
        .df()
        .sort_values("Last_reviewed")
        .reset_index()
    )

    st.write(exercise)
    exercise_name = exercise.loc[0, "exercise_name"]
    with open(f"Answers/{exercise_name}.sql", encoding="utf-8") as f:
        answer = f.read()
    solution_df = con.execute(answer).df()

st.header("Enter your code:")
sql_query = st.text_area(label="Enter an SQL request", key="user_input")
if sql_query:
    result = con.execute(sql_query).df()
    st.dataframe(result)

    if solution_df.shape[0] != result.shape[0]:
        st.write(
            f"Result has {solution_df.shape[0] - result.shape[0]} differences with the solution_df"
        )

    try:
        # set dataframes columns in the same order
        result = result[solution_df.columns]
        st.dataframe(result.compare(solution_df))
    except KeyError as e:
        st.write("Some columns are missing")

tab2, tab3 = st.tabs(["Tables", "Solution"])
with tab2:
    exercise_tables = exercise.loc[0, "tables"]
    for table in exercise_tables:
        st.write("Table ", table)
        table_df = con.execute(f"SELECT * FROM {table}").df()
        st.dataframe(table_df)
with tab3:
    st.text(answer)
