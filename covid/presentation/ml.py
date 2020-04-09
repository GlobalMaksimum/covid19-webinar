import streamlit as st
import numpy as np
from covid.data import load_data

import altair as alt
import pandas as pd
import h2o


def content():
    from h2o.automl import H2OAutoML
    h2o.init()

    st.title("ML View")

    d = load_data()

    st.header("Time Independent Picture")

    with st.echo():
        d_ti = d.copy()
        d_ti['dConfirmed'] = d_ti.groupby(['Country', 'Province'], sort=['Day']). \
            Confirmed.apply(lambda r: r.shift(-1, fill_value=0) - r)
        d_ti['ln_dConfirmed'] = np.log1p(d_ti.dConfirmed)
        d_ti['ln_Confirmed'] = np.log1p(d_ti.Confirmed)

    st.dataframe(
        d_ti.assign(Location=lambda r: r.Country + ', ' + r.Province).query(
            "Location in ('US, New York','Turkey, ')"))

    locs = st.sidebar.multiselect("Locations", d_ti.assign(Location=lambda r: r.Country + ', ' + r.Province).query(
        "dConfirmed > 0").Location.unique())
    ch = alt.Chart(d_ti.assign(Location=lambda r: r.Country + ', ' + r.Province).query(
        "dConfirmed > 0").query(
        "Location in ( {locs} )".format(locs=",".join([f"'{loc}'" for loc in locs])))).transform_window(
        ln_dConfirmed='mean(ln_dConfirmed)', frame=[0, 0], groupby=["Location"]).mark_line().encode(
        x='ln_Confirmed:Q',
        y='ln_dConfirmed:Q',
        tooltip=['Confirmed', 'dConfirmed'],
        color='Location').interactive()

    reference = alt.Chart(
        pd.DataFrame(dict(ln_Confirmed=np.linspace(0, 11), ln_dConfirmed=np.linspace(0, 11)))).mark_line(
        color='gray').encode(
        x='ln_Confirmed:Q',
        y='ln_dConfirmed:Q',
    )

    st.altair_chart(ch + reference, use_container_width=True)

    st.header("A bit of Feature Engineering")

    lags = list(range(1, 21))

    for i in lags:
        d_ti[f'ln_dConfirmed_l{i}'] = d_ti.groupby(['Country', 'Province'], sort=['Day']).ln_dConfirmed.apply(
            lambda x: x.shift(i, fill_value=0))
        d_ti[f'ln_Confirmed_l{i}'] = d_ti.groupby(['Country', 'Province'], sort=['Day']).ln_Confirmed.apply(
            lambda x: x.shift(i, fill_value=0))

    st.dataframe(d_ti)

    st.subheader("Pickup Important Features by Correlation")

    st.dataframe(d_ti[d_ti.Confirmed >= 1].corr().sort_values(['ln_dConfirmed'], ascending=False))

    st.subheader("Training Dataset")
    train = d_ti[
        ['ln_dConfirmed', 'ln_Confirmed', 'Confirmed', 'dConfirmed', 'Day', 'Country', 'Province'] + [
            f'ln_dConfirmed_l{i}' for i in range(1, 12)]].query('dConfirmed >= 0 and Confirmed >= 10').drop(
        ['Day', 'Country', 'Province', 'Confirmed', 'dConfirmed'],
        axis=1)

    train_h2o = h2o.H2OFrame(train)
    st.dataframe(train)

    st.subheader("Test Dataset")
    test = d_ti[
        ['ln_dConfirmed', 'ln_Confirmed', 'Confirmed', 'dConfirmed', 'Day', 'Country', 'Province'] + [
            f'ln_dConfirmed_l{i}' for i in range(1, 12)]].query('dConfirmed < 0 and Confirmed >= 10').drop(
        ['Confirmed', 'dConfirmed', 'ln_dConfirmed'],
        axis=1)

    st.dataframe(test)
    test_h2o = h2o.H2OFrame(test)

    st.subheader("Building a AutoML Model")
    aml = H2OAutoML(max_runtime_secs=30, seed=1, verbosity='info'
                    , nfolds=3
                    , stopping_metric='MSE'
                    , stopping_tolerance=0.001
                    , sort_metric='MSE')

    aml.train(y='ln_dConfirmed', training_frame=train_h2o)

    st.dataframe(aml.leaderboard.as_data_frame())

    test_h2o['y_pred'] = aml.predict(test_h2o).expm1()

    st.subheader("Predictions")
    st.dataframe(test_h2o.as_data_frame())

    h2o.cluster().shutdown()
