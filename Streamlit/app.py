import streamlit as st
from multiapp import MultiApp
from apps import homepage
from apps.Classification_modelling.CT_Image_Detector.main import detect
# from apps.Sentiment_Analysis.sentimentinference import detect1
from apps.Classification_modelling.Covid_Symptoms_Prediction.main import detect2
from apps.Time_Series.forecast import detectf

def main():
    st.sidebar.image("logo.jfif", use_column_width=True)
    app = MultiApp()
    st.markdown("""# Socio-Economic Impact of Covid19""")
    app.add_app("Homepage",homepage.app)
    app.add_app("CT Scan Detector",detect)
    # app.add_app("Sentiment analysis",detect1)
    app.add_app("Covid symptoms",detect2)
    app.add_app("Forecast",detectf)
    app.run()

if __name__ == "__main__":
    main()