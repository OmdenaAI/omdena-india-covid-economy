import streamlit as st
from multiapp import MultiApp
from apps import homepage

def main():

    app = MultiApp()
    st.markdown("""# Welcome to the application for Socio-Economic Impact of Covid19""")
    app.add_app("Homepage",homepage.app)
    #app.add_app("
    app.run()

if __name__ == "__main__":
    main()