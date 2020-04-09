import streamlit as st
from covid.data import load_data
import altair as alt
import numpy as np
import pandas as pd


def content():
    st.title("First 15 days in Turkey after the first Confirmed Case")

    n_days = st.slider("First N Days", 3, 25, 15)

    tr = load_data().query("Country == 'Turkey'").sort_values("Day").head(n_days)[['Day', 'Confirmed']]

    st.dataframe(tr)

    ch = alt.Chart(tr).mark_line().encode(
        x='Day:T',
        y='Confirmed:Q'
    ).interactive()

    st.altair_chart(ch, use_container_width=True)

    st.header("'A' Model: Exponential Family")
    st.markdown("""
    Note that a model is your (datascientist) perception on the what you observe.
    
    > First 15 days of Confirmed cases can be explained by a exponential model.
    
    """)

    st.subheader("Exponential Model")

    st.markdown(r"""
    Assume that model is of the form 
    $$
    y(t) = {\alpha}e^{\beta t}
    $$
    
    * $y(t)$: Number of confirmed cases in $t^{th}$ day.
    * $\alpha$ and $\beta$ controls how we fit the data.
    """)

    st.header(r"Searching for *best/optimal* $\alpha$ and $\beta$")

    st.subheader("Best/Optimal requires a definition of 'optimality'")
    st.markdown(r"""
    > Choose/Find $\alpha$ and $\beta$ such that
    
    > $\sum^{14}_{t=0}{ (y(t) - \hat{y}(t))^2 }$ is minimized
    """)

    st.info(r"""**Claim**: $\alpha$ and $\beta$ that minimizes $\sum^{14}_{t=0}{ (y(t) - \hat{y}(t))^2 }$, also minimizes  $\sum^{14}_{t=0}{ (ln(y(t)) - ln(\hat{y}(t)))^2 }$ because $ln(x)$ is a monotonically increasing continuous function. 
            """)
    st.info(
        r"""**Proof ?**: Take the derivative of both error functions with respect to $\alpha$ and $\beta$ seperately and see that they are the same.""")

    st.subheader(r"Convexity guarantees Global Minimum")
    st.info(
        r"**Claim**: Error function(s) is convex w.r.t. $\alpha$ and $\beta$. In other words best $\alpha$ and $\beta$ is best indeed.")

    st.info(
        r"""**Proof ?**: Proving convexity of a function may sometimes be tricky. But not for these two functions. Refer to [Convex Optimization](https://web.stanford.edu/~boyd/cvxbook/) by *Stephan Boyd and Lieven Vandernberghe*""")
    st.subheader("Exponential Family is Linear")

    st.markdown(r"""
        This model family is actually linear
        $$
        ln(y) = ln({\alpha}) + {\beta t}
        $$
        """)

    if st.checkbox("Show Data"):
        st.dataframe(tr.assign(lnConfirmed=np.log1p(tr.Confirmed)))

    ch = alt.Chart(tr.assign(lnConfirmed=np.log1p(tr.Confirmed))).mark_line().encode(
        x='Day:T',
        y='lnConfirmed:Q'
    ).interactive()

    st.altair_chart(ch, use_container_width=True)

    y = np.log1p(tr.sort_values('Day').Confirmed).values
    t = np.arange(len(y))

    st.markdown(r"""
    Note that and equation of the $y = mx + c$ form can be written as 
    
    $$
     \begin{bmatrix}
       y_0 \\
        \vdots  \\
       y_{N}
        \end{bmatrix} = \begin{bmatrix}
       x_0 & 1 \\
        \vdots & \vdots  \\
       x_N & 1 
        \end{bmatrix} \begin{bmatrix}
       m \\ c
        \end{bmatrix}
    $$
    
    In our case
    
    $$
     \begin{bmatrix}
       ln(y_0) \\
       ln(y_1) \\
        \vdots  \\
       ln(y_{14})
        \end{bmatrix} = \begin{bmatrix}
       0 & 1 \\
       1 & 1 \\
        \vdots & \vdots  \\
       14 & 1 
        \end{bmatrix} \begin{bmatrix}
        \beta \\ ln(\alpha) 
        \end{bmatrix}
    $$
    
    """)

    st.markdown(r"""
    
    """)

    with st.echo():
        A = np.vstack([t, np.ones(len(y))]).T

        (beta, ln_alpha), res = np.linalg.lstsq(A, y)[0:2]



    st.markdown(r"Optimal $\beta$ = {beta:.3f} and $\alpha$ = {alpha:.3f} with residual {res:.3f}".format(beta=beta,alpha=np.expm1(ln_alpha),res=res[0]))


    p = pd.DataFrame(dict(Day=tr.sort_values('Day').Day, lny_true=y, lny_pred=t * beta + ln_alpha))

    ch = alt.Chart(p.assign(y_pred=lambda x: np.expm1(x.lny_pred),
                            y_true=lambda x: np.expm1(x.lny_true))).transform_fold(
        ['y_true', 'y_pred']).mark_line().encode(
        x='Day:T',
        y='value:Q',
        color='key:N'
    ).interactive()

    st.altair_chart(ch, use_container_width=True)

    st.markdown(r"""
    $$
    \frac{y_{t+1}}{y_t} = \frac{{\alpha}e^{\beta (t+1)}}{{\alpha}e^{\beta t}} = e^{\beta} = %f
    $$
    """%np.exp(beta))

    st.markdown("Check [np.linalg.lstsq](https://docs.scipy.org/doc/numpy/reference/generated/numpy.linalg.lstsq.html) documentation for more details.")
