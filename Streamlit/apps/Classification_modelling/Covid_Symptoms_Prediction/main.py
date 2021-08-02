import os
import shutil
import time

import numpy as np
import streamlit as st
import xgboost as xgb


def predictCovid(inputArray):
    count0 = 0
    count1 = 0
    for i in range(1, 9):
        model_load = xgb.XGBClassifier()
        model_load.load_model("apps/Classification_modelling/Covid_Symptoms_Prediction/models/model" + str(i) + ".json")
        result = model_load.predict(inputArray.reshape((1, 8)))
        if result[0] == 1:
            count1 += 1
        else:
            count0 += 1
    if count1 >= count0:
        return True
    else:
        return False

def detect2():
    st.title('Covid19 Symptoms Analysis')
    st.write("")
    st.write("Answer these questions")
    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
    # c1, c2 = st.beta_columns([2, 1])

    # with c1:
    cough = st.radio("Do you cough often?", ('YES', 'NO'))
    st.write("")
    fever = st.radio("Do you have Fever?", ('YES', 'NO'))
    st.write("")
    sore_throat = st.radio("Noticed Sore Throat?", ('YES', 'NO'))
    st.write("")
    breath = st.radio("Problem in Breathing?", ('YES', 'NO'))
    st.write("")
    head_ache = st.radio("Head Ache?", ('YES', 'NO'))
    st.write("")
    age = st.radio("Is your age above 60?", ('YES', 'NO'))
    st.write("")
    gender = st.radio("Gender?", ('MALE', 'FEMALE'))
    st.write("")
    test = st.radio("Test Indication (NO = Abroad, YES = Contact with confirmed and OTHER = Other)", ('YES', 'NO', 'OTHER'))

    if st.button("Predict"):
        st.write("Processing...")
        mp = {'YES':1, 'NO':0, 'OTHER':2, 'MALE':1, 'FEMALE':0}
        result = np.array([
                        mp[cough],
                        mp[fever],
                        mp[sore_throat],
                        mp[breath],
                        mp[head_ache],
                        mp[age],
                        mp[gender],
                        mp[test],])

        result = predictCovid(result)
        st.write("Looks like you are affected by Covid19") if result else st.write("Looks like you aren't affected by Covid19")