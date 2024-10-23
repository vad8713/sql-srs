## pylint: disable=missing-module-docstring
import io
import ast
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
#    st.write(exercise)

    exercise_name = exercise.loc[0, "exercise_name"]
    with open(f"Answers/{exercise_name}.sql", "r") as f:
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
    exercise_tables = ast.literal_eval(exercise.loc[0,"tables"])
    for table in exercise_tables:
        st.write("Table ",table)
        table_df = con.execute(f"SELECT * FROM {table}").df()
        st.dataframe(table_df)
with tab3:
     st.text(answer)
