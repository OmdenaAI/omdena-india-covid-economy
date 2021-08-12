import streamlit as st

from apps.Time_Series.mortality_rate.mortality import mainf
from apps.Time_Series.vaccine.predict import mainv
from apps.Time_Series.unemployment.predict import mainu
from apps.Time_Series.economy.new import new


def detectf():
    st.sidebar.header('Domain:')
    choice = st.sidebar.selectbox('Choice:', ('Economy','Mortality Rate', 'Unemployment Rate', 'Vaccine Rate'))

    if (choice == 'Mortality Rate'):
        mainf()
    elif(choice == 'Unemployment Rate'):
        mainu()
    elif(choice == 'Vaccine Rate'):
        mainv()
    elif(choice == 'Economy'):
        new()