import streamlit as st

from covid.data import load_data
import numpy as np
import altair as alt


@st.cache
def load_proxy():
    d = load_data()

    return d


def illustrate(d, with_data=False):
    ch = alt.Chart(d).transform_fold(['Active', 'Deaths', 'Recovered'], as_=['type', 'count']).mark_point(size=30,
                                                                                                          opacity=0.6).encode(
        x='Day:T',
        y='count:Q',
        tooltip=['Day', 'count:Q', 'type:N'],
        color='type:N').interactive()

    st.altair_chart(ch, use_container_width=True)

    if with_data:
        st.dataframe(d.sort_values("Day"))


def content():
    st.title("Data Access and Visualize")
    st.markdown("""
    * [CSSEGISandData COVID-19 Github Repository](https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports)
    """)

    d = load_proxy()

    st.dataframe(d.head())

    st.header("Top 10 Countries by Peak **Active** Cases")
    with st.echo():
        top10 = d.groupby(['Country']).Active.max().reset_index() \
            .sort_values('Active', ascending=False) \
            .head(10)

    st.dataframe(top10)

    st.header("A Few Important Country/Province to Note")
    st.markdown("""
    Note that some provinces in China already had a bell shape curve for number of **Active** cases, whereas 
    many European countries are in the growing phase, including Turkey.
    """)

    with st.echo():
        ch = alt.Chart(d) \
            .transform_fold(['Active', 'Deaths', 'Recovered'], as_=['type', 'count']) \
            .mark_point(size=30, opacity=0.6) \
            .encode(x='Day:T', y='count:Q',
                    tooltip=['Day', 'count:Q', 'type:N'],
                    color='type:N') \
            .interactive()

    st.subheader("Hubei Stats")
    illustrate(d.query("Province == 'Hubei' "))

    st.subheader("Hunan Stats")
    illustrate(d.query("Province == 'Hunan' "))

    st.subheader("Italy Stats")
    illustrate(d.query("Country == 'Italy' "))

    st.subheader("Spain Stats")
    illustrate(d.query("Country == 'Spain' "))

    st.subheader("Germany Stats")
    illustrate(d.query("Country == 'Germany' "))

    st.subheader("Germany Stats")
    illustrate(d.query("Province == 'New York' "), with_data=True)

    st.subheader("Turkey Stats")
    illustrate(d.query("Country == 'Turkey' "))
