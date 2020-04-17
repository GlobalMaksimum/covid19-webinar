import streamlit as st
import numpy as np
from covid.data import load_data

import altair as alt
from scipy.integrate import odeint
from scipy.optimize import curve_fit
import pandas as pd


@st.cache
def load_proxy():
    d = load_data()

    return d


def content():
    st.title("Modeling COVID-19 using SIR")

    dd = load_proxy().assign(Location=lambda r: r.Country + ', ' + r.Province)

    st.sidebar.subheader("Region Selector")
    country = st.sidebar.radio("Top 10 Countries by Peak Active Cases",
                               dd.groupby('Country').Active.max().reset_index().sort_values('Active',
                                                                                            ascending=False).head(8)[
                                   'Country'].unique(), 6)

    ss = dd.query(f"Country == '{country}'")

    if len(ss) > 1:
        province = st.sidebar.selectbox("Provinces",
                                        ss.Province.unique())

        d = ss.query(f"Province == '{province}' ").copy()
    else:
        d = ss.copy()

    d_SIR = d[['Day', 'Active', 'Deaths', 'Recovered']].copy().reset_index(drop=True)

    min_N = int(d.Active.max())
    max_N = int(d.Active.max() * 1000)
    init_N = int(min_N * 2)

    N = st.sidebar.slider("Population Size", min_N, max_N, init_N, 10_000)

    if province:
        st.header(f"John Hopkins Data for {province}, {country}")
    else:
        st.header(f"John Hopkins Data for {country}")

    st.dataframe(d_SIR)

    st.header("Converting data to SIR Model")

    with st.echo():
        d_SIR['S'] = N - d_SIR.Active - d_SIR.Deaths - d_SIR.Recovered
        d_SIR['I'] = d_SIR.Active
        d_SIR['R'] = d_SIR.Deaths + d_SIR.Recovered

    st.markdown(f"Population has taken to be **{N}**. Use the slider to change it.")

    st.dataframe(d_SIR.drop(['Active', 'Deaths', 'Recovered'], axis=1))

    # ch = alt.Chart(d).transform_fold(['Active', 'Deaths', 'Recovered'], as_=['type', 'count']).mark_point(size=30,
    #                                                                                                       opacity=0.6).encode(
    #     x='Day:T',
    #     y='count:Q',
    #     tooltip=['Day', 'count:Q', 'type:N'],
    #     color='type:N').interactive()
    #
    # st.altair_chart(ch, use_container_width=True)

    ch = alt.Chart(d_SIR).transform_fold(['I', 'R'], as_=['status', 'count']).mark_point(size=30,
                                                                                         opacity=0.6).encode(
        x='Day:T',
        y='count:Q',
        tooltip=['Day', 'count:Q', 'status:N'],
        color='status:N').interactive()

    st.altair_chart(ch, use_container_width=True)

    st.header("Curve Fitting")
    curve_fitting()

    st.header("SIR Model")
    S0, I0, R0 = list(d_SIR.S)[0], list(d_SIR.I)[0], list(d_SIR.R)[0]

    ode(S0, I0, R0)

    def sir_ode(SIR, t, beta, gamma, N):
        S, I, R = SIR

        dS = -beta * ((S * I) / N)
        dI = beta * ((S * I) / N) - gamma * I
        dR = gamma * I

        dydt = [dS, dI, dR]

        return dydt

    def opti(t, _beta, _gamma):
        y0 = [S0, I0, R0]

        sol = odeint(sir_ode, y0, t, args=(_beta, _gamma, S0 + I0 + R0))

        return np.hstack((sol[:, 1], sol[:, 2]))
        #return sol[:, 1]

    # st.dataframe(d_SIR.head())

    # popt, pcov = curve_fit(opti, t, np.hstack((d_SIR.I.to_numpy(), d_SIR.R.to_numpy())), bounds=(0, [np.inf, 1]))

    st.subheader(r"Optimize $\beta$, $\gamma$")
    st.markdown(r"""
    $\beta$, $\gamma$ parameters can be optimized based on data using by combining `curve_fit` and `odeint`.
    """)
    t = np.arange(len(d_SIR))
    #popt, pcov = curve_fit(opti, t, d_SIR.I.to_numpy(), bounds=(0, [np.inf, 1]))
    popt, pcov = curve_fit(opti, t, np.hstack((d_SIR.I.to_numpy(), d_SIR.R.to_numpy())), bounds=(0, [np.inf, 1]))

    beta, gamma = popt[0], popt[1]

    st.markdown(r">%s %s optimal paramaters found to be $\beta$ = %.2f and $\gamma$ = %.2f " % (province, country, beta, gamma))

    ch = alt.Chart(pd.DataFrame(dict(t=t, I=d_SIR.I))).mark_point(size=30, opacity=0.6,
                                                                  color="#512b58").encode(
        x='t:Q',
        y='I:Q').interactive()

    sol = odeint(sir_ode, [S0, I0, R0], t, args=(beta, gamma, N))

    chP = alt.Chart(pd.DataFrame(dict(t=t, I=sol[:, 1]))).mark_line(color="#3b6978").encode(
        x='t:Q',
        y='I:Q').interactive()

    st.altair_chart((ch + chP), use_container_width=True)

    ch = alt.Chart(pd.DataFrame(dict(t=t, R=d_SIR.R))).mark_point(size=30, opacity=0.6,
                                                                  color="#512b58").encode(
        x='t:Q',
        y='R:Q').interactive()

    chP = alt.Chart(pd.DataFrame(dict(t=t, R=sol[:, 2]))).mark_line(color="#3b6978").encode(
        x='t:Q',
        y='R:Q').interactive()

    st.altair_chart((ch + chP), use_container_width=True)


def ode(S0, I0, R0):
    st.subheader("System of ODE")
    st.markdown(r"""
    Each susceptible member of population (there are $S$ of them) can be infected by one of $I$ infected member with probability $\beta$ at time $t$
    
    $\frac{dS}{dt} = -\beta \frac{S(t)I(t)}{N}$
    
    The number of new infected members will be determined by above equations, where existing members will be cured or will die with probabilty $\gamma$
    
    $\frac{dI}{dt} = \beta \frac{S(t)I(t)}{N} - \gamma I(t)$
    
    Any intected member (there are $I$ of them) will be cured or will die with probabilty $\gamma$
    
    $\frac{dR}{dt} = \gamma I(t)$
    """)
    st.subheader("Python")
    with st.echo():
        def sir_ode(SIR, t, beta, gamma, N):
            S, I, R = SIR

            dS = -beta * ((S * I) / N)
            dI = beta * ((S * I) / N) - gamma * I
            dR = gamma * I

            dydt = [dS, dI, dR]

            return dydt

        y0 = [S0, I0, R0]

    st.markdown(r"""
    Given
    * derivatives
    * initial conditions
    
    $S(t)$, $I(t)$ and $R(t)$ can numerically be solved by `odeint` function in `scipy.integrate` 
    module for a given $\beta$ and $\gamma$.
    
    Try different $\beta$ and $\gamma$ values using sliders
    """)

    _beta = st.slider("Beta", 0., 10., 0.5, 0.01)
    _gamma = st.slider("Gamma", 0., 1.0, 0.1, 0.01)
    # st.write(y0)
    t = np.arange(100)
    sol = odeint(sir_ode, y0, t, args=(_beta, _gamma, S0 + I0 + R0))

    d = pd.DataFrame(sol)
    d.columns = ['S', 'I', 'R']
    d['t'] = t

    ch = alt.Chart(d).transform_fold(['S', 'I', 'R'], as_=['state', 'population']).mark_line(opacity=0.6,
                                                                                             size=3).encode(
        x='t:Q',
        y='population:Q', color=alt.Color('state:N',
                                          scale=alt.Scale(
                                              domain=['S', 'I', 'R'],
                                              range=['blue', 'red', 'green'])),
        tooltip=['state:N', 'population:Q', 't:Q']).interactive()
    st.altair_chart(ch, use_container_width=True)

    # st.write(d)


def curve_fitting():
    st.markdown("Assume that we have some data generated by some process")

    var_scale = st.slider("Noise Variance Scaling", 0., 3., 0.2, 0.1)

    st.subheader("Equation")
    st.markdown("""
    $$y = ae^{-bx} + c + N(0, \sigma)$$
    
    $$a=2.5, b=1.3, c=0.5$$
    """)

    st.subheader("Python")
    with st.echo():
        def y(x, a, b, c):
            return a * np.exp(-b * x) + c

    xdata = np.linspace(0, 4, 100)
    ydata = y(xdata, 2.5, 1.3, 0.5)
    np.random.seed(1729)

    y_noise = var_scale * np.random.normal(size=xdata.size)
    ydata = ydata + y_noise
    ch_data = alt.Chart(pd.DataFrame(dict(xdata=xdata, ydata=ydata))).mark_point(size=30,
                                                                                 color="#a5a73f").encode(
        x='xdata:Q',
        y='ydata:Q').interactive()

    st.markdown("""
    `curve_fit` function in `scipy.optimize` module can be used to find optimal $a$ and $b$ parameters.
    
    """)
    popt, pcov = curve_fit(y, xdata, ydata)

    st.markdown(f"Optimal parameters $a$={popt[0]:.2f}, $b$={popt[1]:.2f} and $c$={popt[2]:.2f}")

    ch_pred = alt.Chart(pd.DataFrame(dict(xdata=xdata, ydata=y(xdata, *popt)))).mark_line(color="#eb8050").encode(
        x='xdata:Q',
        y='ydata:Q').interactive()

    ch_true = alt.Chart(pd.DataFrame(dict(xdata=xdata, ydata=y(xdata, 2.5, 1.3, 0.5)))).mark_line(
        color="#488f31").encode(
        x='xdata:Q',
        y='ydata:Q').interactive()

    ch_noise = alt.Chart(pd.DataFrame(dict(Noise=var_scale * np.random.normal(size=10_000)))).mark_boxplot().encode(
        y='Noise:Q',
    ).properties(width=100)

    st.altair_chart((ch_data + ch_pred + ch_true) | ch_noise, use_container_width=True)
