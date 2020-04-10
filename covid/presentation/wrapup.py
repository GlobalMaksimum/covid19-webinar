import streamlit as st


def content():
    st.balloons()

    st.title("From Here...")

    st.markdown(":facepunch: Appreciated for your time today. ")
    st.header("Clone")
    st.markdown("""
    * `git clone` from GitHub.
    * Run the code we provide.
""")
    st.header("Code")
    st.markdown("""
    * Use it as a baseline for your own work.
      * No way to learn a thing by watching.
    """)

    st.header("Fix")
    st.markdown("""
    * Open an issue to us in case that something is wrong.
    * Or better, fix and send a pull request
    """)

    st.header("Improve")
    st.markdown("""
     * Come up with your own chapter
     * Fork it or send a pull request.
     """)

    st.header("Collaborate")
    st.markdown("""
    * Maybe next time we can present together.
    """)
