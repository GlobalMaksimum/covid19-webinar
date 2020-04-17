import streamlit as st


def content():
    st.title("Toolbox")

    st.header("Math Toolbox")
    st.markdown("""
    * Basic Understanding of Probability and Statistics
    * Calculus 101 
    * Fundamental Machine Learning
    """)
    st.header("Python Toolbox")

    st.subheader("Python")
    st.image("https://www.python.org/static/community_logos/python-logo-master-v3-TM.png", width=180)
    st.markdown("""
    We do depend on **Python 3.7**
    
    * Function parameter & return type annotations (this is **Python 3.6**, I guess)
      * Also a few variable type annotations (much less frequently)
    """)
    with st.echo():
        from typing import List, Tuple

        def func(p_a: int, p_b: str, p_c: float) -> Tuple[int, str, float]:
            return p_a, p_b, p_c

        a: int = 1
        b: str = "Hello"
        c: float = 2.0

        v = func(a, b, c)

    st.markdown("* `f-string` allows us to interpolate variables into strings.")
    with st.echo():
        s = f"func({a}, {b}, {c}) returns a tuple with value {v}"
    st.markdown(s)

    st.markdown("""
    * Thousand separator notation for constants
    """)
    with st.echo():
        myflumsy_variable = 100_000  # instead of myflumsy_variable = 100000

    st.markdown("""
    * And some more which I don't remember :blush:
    """)

    st.subheader("streamlit")
    st.markdown("You are currently looking at it.")
    st.image("https://pbs.twimg.com/profile_images/1234856290058428416/8lWJhqj1_400x400.jpg",
             width=80)
    st.subheader("pandas")
    st.markdown("All data loading and manipulation")
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/e/ed/Pandas_logo.svg/1200px-Pandas_logo.svg.png",
             width=100)
    st.subheader("numpy")
    st.markdown("""
    * Any vector, matrix or multidimentional array operations.
    * Least Square (lstsq) Regression Solver
    """)
    st.image("https://user-images.githubusercontent.com/1217238/65364991-9f0fcb80-dbca-11e9-89a1-f369aa2be57a.png",
             width=100)

    st.subheader("scipy")
    st.markdown("`curve_fit` for parameter optimization and `odeint` for ordinary differential equation solving")
    st.image("https://www.fullstackpython.com/img/logos/scipy.png",
             width=80)

    st.markdown(r"### $H_2O$ AutoML")
    st.markdown("You are currently looking at it.")
    st.image("https://i0.wp.com/sefiks.com/wp-content/uploads/2019/09/h2o-automl.jpg?fit=835%2C900&ssl=1",
             width=60)

    st.title("Table of Content")
    st.header("Introduction to COVID Data")
    st.markdown("""
    * Loading data from web
      * Caching into Parquet files
    * Time variant visualization of COVID data using altair
    * Parametrization of charts using streamlit capabilities
    * Time invariant visualization of COVID data
    """)
    st.header("Early Phase Analysis of Epidemics using Exponential Model")
    st.markdown("""$$
    y(t) = A_{i}e^{B_{i}t}
    $$
    """)

    st.markdown("* **Claim**: Exponential models are **linear** models")
    st.markdown("* Learn for $A_{i}$ & $B_{i}$ using data")

    st.header("ML based model to Predict the Next Day")
    st.subheader("Feature Engineering")

    # st.balloons()
