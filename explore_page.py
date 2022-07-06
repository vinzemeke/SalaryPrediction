import math
import pickle
from operator import index

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
from matplotlib.style import use
from st_aggrid import AgGrid

from predict_page import predict

st.set_page_config(layout="wide")


# loading the model:
def load_model():
    with open("saved_steps.pk1", "rb") as file:
        data = pickle.load(file)
    return data


# load the cleaned dataset from pickle:
def load_data():
    with open("cleandata.pkl", "rb") as file:
        df = pd.DataFrame(pickle.load(file))
    return df


df = load_data()


# DATA WRANGLING BITS
# average salaries per country:
mean_by_country = df.groupby(["Country"])["Salary"].mean().sort_values(ascending=True)
mean_by_country = pd.DataFrame(mean_by_country)
mean_by_country.reset_index(inplace=True)
mean_by_country.sort_values("Country")
mean_by_country["Salary"] = mean_by_country["Salary"].astype(int)


median_by_country = (
    df.groupby(["Country"])["Salary"].median().sort_values(ascending=True)
)
median_by_country = pd.DataFrame(median_by_country)
median_by_country.reset_index(inplace=True)
median_by_country.sort_values("Country")
median_by_country["Salary"] = median_by_country["Salary"].astype(int)


## METHODS
def truncate(f, n):
    return math.floor(f * 10**n) / 10**n


def display_salary_prog(country, edLevel, max_year):
    model = load_model()
    # get the data for each year:
    salary = {}
    for i in range(max_year + 1):
        salary[i] = predict(country, edLevel, i)
    return salary


def compare_salaries(countries, edLevel, year):
    salary = {}
    for i in range(len(countries)):
        salary[countries[i]] = predict(countries[i], edLevel, year)
    return salary


def compare_salary_progression(countries, edLevel, years):
    salary = []
    for i in countries:
        for j in range(years + 1):
            builder = []
            predicted = predict(i, edLevel, j)
            builder.extend((i, j, predicted))
            print(builder)
            salary.append(builder)
    return pd.DataFrame(salary, columns=("Country", "Experience", "Salary"))


def single_year_multiple_countries(countries, edLevel, year):
    result = {}
    for i in countries:
        pred_sal = predict(i, edLevel, year)
        result[i] = truncate(pred_sal, 0)
    result = pd.DataFrame.from_dict(result, orient="index")
    result = result.reset_index(drop=False)
    result.columns = ["Country", "Salary"]
    result.style.set_precision(0)
    return result


def show_explore_page():
    st.header("Explore Software Engineer Salaries")
    st.markdown(
        """<hr style="height:0.5px;
                    border:none;color:#333;
                    background-color:#123;" /> """,
        unsafe_allow_html=True,
    )
    container1 = st.container()
    container1.markdown("##### Average Reported Salaries per Country")
    expander1 = container1.expander("Average Reported Salaries by Country")

    with expander1:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("Average Salaries By Country")
            AgGrid(mean_by_country)

        with c2:
            st.markdown("Median Salaries by country")
            a = AgGrid(median_by_country)

        st.markdown(
            """<hr style="height:0.5px;
                    border:none;color:#333;
                    background-color:#123;" /> """,
            unsafe_allow_html=True,
        )

        st.markdown("### View Salaries (in USD)")
        options = ["Average Salaries", "Median Salaries"]
        selected = st.radio("  ", options)

        if selected == "Average Salaries":
            fig = px.bar(
                mean_by_country,
                x="Country",
                y="Salary",
                color="Salary",
                title="Average Salaries",
                color_discrete_sequence=px.colors.sequential.Plasma_r,
                height=750,
            )
            st.plotly_chart(figure_or_data=fig, use_container_width=True)

        else:
            fig = px.bar(
                median_by_country,
                x="Country",
                y="Salary",
                color="Salary",
                title="Median Salaries",
                color_discrete_sequence=px.colors.sequential.Plasma_r,
                height=750,
            )
            st.plotly_chart(figure_or_data=fig, use_container_width=True)

    container2 = st.container()
    container2.markdown("##### Compare Projected Salaries by Country")
    expander2 = container2.expander("Compare Projected Salaries By Country")

    with expander2:
        col1, col2 = st.columns(2)

        with col1:
            selected_countries = st.multiselect(
                "Select Countries to Compare (multiple selections allowed)",
                sorted(df["Country"].unique()),
                default=["Australia", "Brazil"],
            )

        with col2:
            years = st.slider("Years of Experience", 0, 30, 3, 1)
            education = st.selectbox(
                "Level of Education", sorted(df["EdLevel"].unique())
            )

        compare = st.button("Compare")

        st.markdown(
            """<hr style="height:0.1px;
                    border:none;color:#333;
                    background-color:#123;" /> """,
            unsafe_allow_html=True,
        )

        if compare:
            col3, col4 = st.columns(2)
            with col3:
                st.caption(
                    "##### Education: {}    |    Years of Experience: {:.0f}".format(
                        education, years
                    )
                )
                barchart_data = single_year_multiple_countries(
                    selected_countries, education, years
                )
                fig = px.bar(
                    barchart_data,
                    x="Salary",
                    y=("Country"),
                    color="Country",
                    title="Predicted Salary",
                )
                st.plotly_chart(fig, use_container_width=True)

            with col4:
                st.caption("##### Predicted Salary Growth Curve")
                line_data = compare_salary_progression(
                    selected_countries, education, years
                )
                fig2 = px.line(
                    line_data,
                    x="Experience",
                    y="Salary",
                    color="Country",
                    markers=True,
                    title="Predicted Salary Growth Curve",
                )
                st.plotly_chart(fig2, use_container_width=True)
