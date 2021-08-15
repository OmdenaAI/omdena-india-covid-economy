import streamlit as st

# from apps.Time_Series.download import load

from apps.Time_Series.mortality_rate.mortality import mainf
from apps.Time_Series.vaccine.predict import mainv
from apps.Time_Series.unemployment.predict import mainu
from apps.Time_Series.sensex.new import new
from apps.Time_Series.gdp.gdp import maing
from apps.Time_Series.industrial_production.industrial_production import maini

st.cache(suppress_st_warning=True)
def detectf():
    # load()
    st.sidebar.header('Domain:')
    choice = st.sidebar.selectbox('Choice:', ('Economy','Mortality Rate', 'Unemployment Rate', 'Vaccine Rate', "GDP Analysis", "Industrial Production Rate Analysis"))

    if (choice == 'Mortality Rate'):
        mainf()
    elif(choice == 'Unemployment Rate'):
        mainu()
    elif(choice == 'Vaccine Rate'):
        mainv()
    elif(choice == 'Economy'):
        new()
    elif(choice == 'GDP Analysis'):
        maing()
    elif(choice == 'Industrial Production Rate Analysis'):
        maini()