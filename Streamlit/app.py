import streamlit as st
from multiapp import MultiApp
from apps import homepage
from apps.Classification_modelling.CT_Image_Detector.main import detect
from apps.Sentiment_Analysis.sentimentinference import detect1

def main():

    app = MultiApp()
    st.markdown("""# Welcome to the application for Socio-Economic Impact of Covid19""")
    app.add_app("Homepage",homepage.app)
    app.add_app("CT Scan Detector",detect)
    app.add_app("Sentiment analysis",detect1)
    app.run()

if __name__ == "__main__":
    main()