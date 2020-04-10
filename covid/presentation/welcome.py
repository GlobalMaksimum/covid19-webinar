import streamlit as st


def content():
    st.title("Before we Start")

    st.header("Your Hosts Today")
    st.markdown("""
       * **Husnu Sensoy** as the main presenter for today.
       * **Dorukhan Afacan**
         * :fearful: Fixing my potential errors
         * :sweat: Helping me in case of an unexpected code result 
         * :question: Gathering up questions 
       * **Hakan Atilgan**
         * :blush: Anything else
         * :email: [hakan.atilgan@globalmaksimum.com](hakan.atilgan@globalmaksimum.com)
       """)

    st.header("Flow")
    st.markdown("""
    * No powerpoint slides.
    * Real data, real code, real execution.
    * Codes are available in [globalmaksimum GitHub account](https://github.com/GlobalMaksimum/covid19-webinar.git) now.
    * Screen is split into two parts:
      * **LHS**: *PyCharm Community Edition* to edit Python codes.
      * **RHS**: *Streamlit Server* showing you the results of things I do.
        * Just like Jupyter notebook, but with a different flavour.
    """)

    st.header("Polls")
    st.markdown("""
       * Join our polls to help us better understand how we are doing.
       * They are not for you, but for us.
       """)

    st.header("Q&A")
    st.markdown("""
       * Please use **Q&A** button to ask your questions.
       * **@dorukhan** will be taking care of them.
       """)
