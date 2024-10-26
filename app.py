## pylint: disable=missing-module-docstring
## pylint: disable=exec-used

import logging
import os
from datetime import date, timedelta

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


def check_query(user_query: str) -> None:
    """
    Check user query string by comparison of
    1 : columns
    2 : values
    :param user_query: A sting containing the query inserted by the user
    """
    result = con.execute(user_query).df()
    st.dataframe(result)
    try:
        # set dataframes columns in the same order
        result = result[solution_df.columns]
        st.dataframe(result.compare(solution_df))
        if result.compare(solution_df).shape == (0, 0):
            st.write("Correct")
    except KeyError:
        st.write("Some columns are missing")

    n_lines_differences = result.shape[0] - solution_df.shape[0]
    if n_lines_differences != 0:
        st.write(f"Result has {n_lines_differences} differences with the solution_df")


con = duckdb.connect("Data/exercises_sql_tables.db", read_only=False)

st.write(
    """
SQL SRS
Space Repetition System SQL Practice
"""
)

with st.sidebar:

    availableThemes = con.execute("SELECT DISTINCT theme FROM memory_state").df()
    themeLlist = availableThemes["theme"].tolist()
    theme = st.selectbox(
        "What would you like to review",
        themeLlist,
        index=None,
        placeholder="Select a theme",
    )

    if theme:
        st.write("You selected", theme)
        SELECT_THEME_STRING = f"SELECT * FROM memory_state WHERE theme = '{theme}'"
    else:
        SELECT_THEME_STRING = "SELECT * FROM memory_state"

    exercise = (
        con.execute(SELECT_THEME_STRING).df().sort_values("Last_reviewed").reset_index()
    )

    st.write(exercise)
    exercise_name = exercise.loc[0, "exercise_name"]
    with open(f"Answers/{exercise_name}.sql", encoding="utf-8") as f:
        answer = f.read()
    solution_df = con.execute(answer).df()

st.header("Enter your code:")

sql_query = st.text_area(label="Enter an SQL request", key="user_input")

if st.button("Reset"):
    con.execute("UPDATE memory_state SET Last_reviewed = '1970-01-01'")
    st.rerun()

for n_days in [2, 7, 21]:
    if st.button(f"Repeat in {n_days} Days"):
        nextLastReviewed = date.today() + timedelta(days=n_days)
        con.execute(
            f"UPDATE memory_state SET Last_reviewed = '{nextLastReviewed}' WHERE exercise_name = '{exercise_name}'"
        )
        st.rerun()

if sql_query:
    check_query(sql_query)

tab2, tab3 = st.tabs(["Tables", "Solution"])
with tab2:
    exercise_tables = exercise.loc[0, "tables"]
    for table in exercise_tables:
        st.write("Table ", table)
        table_df = con.execute(f"SELECT * FROM {table}").df()
        st.dataframe(table_df)
with tab3:
    st.text(answer)
