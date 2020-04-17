from covid.presentation import *
import streamlit as st
import datetime
from math import ceil

# st.sidebar.title("COVID-19 Data Analysis")
st.sidebar.image('resources/coronavirus64.png')

now = datetime.datetime.now()
end = datetime.datetime.strptime("09-04-2020 18:30", "%d-%m-%Y %H:%M")

sec_left = (end - now).total_seconds()
# st.sidebar.markdown(sec_left)
if sec_left < 0:
    st.sidebar.progress(100)
    st.sidebar.warning("Time is up")
else:
    if sec_left >= 3600:
        st.sidebar.progress(0)
        st.sidebar.info(f"We have {sec_left // 60} min to go")
    else:
        st.sidebar.progress(ceil(((3600 - sec_left) * 100) / 3600))

        if sec_left <= 120:
            st.sidebar.warning("In last 2 min")
        elif sec_left <= 300:
            st.sidebar.warning("In last 5 min")

chapters = ("Welcome on Board",
            "Global Maksimum AI Team COVID Journey",
            "Abstract",
            "Loading COVID Data",
            "Exponential Models",
            "SIR",
            "ML Models",
            "Wrap-up")

callable_dict = {"Welcome on Board": welcome,
                 "Abstract": toc,
                 "Loading COVID Data": dataload,
                 "Wrap-up": wrapup,
                 "Exponential Models": expo,
                 "SIR": SIR,
                 "ML Models": ml,
                 "Global Maksimum AI Team COVID Journey": gm}

st.sidebar.title("Content")

st.sidebar.subheader("Today's Agenda")

part = st.sidebar.radio("", chapters)

callable_dict.get(part, lambda: None)()
