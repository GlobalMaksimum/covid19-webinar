import streamlit as st
import pandas as pd
from io import StringIO
import numpy as np
import altair as alt


def content():
    st.title("Global Maksimum Journey on COVID-19")

    st.image('resources/challange.png', width=900)

    st.header("How to Start a Challange")

    st.markdown("""
    * Define the problem
    * Define time  horizon
    * Define metric
    """)

    st.header("As of Today")

    data = """
    Day	y_true	y_askar	y_dorukhan	y_hilal	y_husnu
19.03.2020	359	324	285	328	237
20.03.2020	670	645	665	636	610
21.03.2020	947	1182	1274	1155	
22.03.2020	1236	1251		1236	1227
23.03.2020	1529	1480	1608	1681	1629
24.03.2020	1872	1708		1857	1860
25.03.2020	2433	2180	2130	2244	2265
26.03.2020	3629	2885	3000	2968	3006
27.03.2020	5698			4754	4668
28.03.2020	7402	7685	7518	7213	7557
29.03.2020	9217	10429	9282	9411	9636
30.03.2020	10827	11852	11766	11708	11991
31.03.2020	13531	12726	12863	12689	12446
01.04.2020	15679	16413	16545	16380	15669
02.04.2020	18135	18160	18645	18132	18203
03.04.2020	20921	20782		21151	
04.04.2020	23934	23807	23705	23898	23450
05.04.2020	27069	27018	27354	27392	27400
06.04.2020	30217	30547	30835	30504	30178
07.04.2020	34109		33465	33536	33434
    """

    df = pd.read_csv(StringIO(data), delim_whitespace=True)

    df['Day'] = pd.to_datetime(df.Day, format='%d.%m.%Y')

    st.dataframe(df.sort_values('Day', ascending=False))

    err_askar = np.abs((df.y_true - df.y_askar) / df.y_true).mean()
    err_dorukhan = np.abs((df.y_true - df.y_dorukhan) / df.y_true).mean()
    err_husnu = np.abs((df.y_true - df.y_husnu) / df.y_true).mean()
    err_hilal = np.abs((df.y_true - df.y_hilal) / df.y_true).mean()

    st.markdown(f"Askar Error(%): {err_askar:.4f}")
    st.markdown(f"Dorukhan Error(%): {err_dorukhan:.4f}")
    st.markdown(f"Husnu Error(%): {err_husnu:.4f}")
    st.markdown(f"Hilal Error(%): {err_hilal:.4f}")

    ch = alt.Chart(df) \
        .transform_fold(['y_true', 'y_hilal', 'y_husnu', 'y_askar', 'y_dorukhan'], as_=['type', 'value']) \
        .mark_line() \
        .encode(x='Day:T', y='value:Q',
                tooltip=['Day', 'value:Q'],
                color='type:N') \
        .interactive()

    st.altair_chart(ch, use_container_width=True)
