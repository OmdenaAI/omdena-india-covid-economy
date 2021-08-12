from __future__ import absolute_import, division, print_function, unicode_literals

import seaborn as sns

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import os
import datetime
import requests

import pandas as pd
import plotly.express as px

from fbprophet import Prophet
import streamlit as st

from apps.Time_Series.mortality_rate.data import jsonToCsv

def mainf():
    url = "https://api.covid19india.org/v4/min/timeseries.min.json"
    req = requests.get(url)
    url_content = req.json()

    df = jsonToCsv(url_content)
    st.title('Mortality Rate Forecasting')
    st.markdown('This page allows you to check forecast of mortality rate from the selected date due to covid19.')
    st.markdown('Due to Covid19, death rate has been increasing gradually since 2020, the worst pandemic ever the world had seen.')
    st.sidebar.header("Date:")
    split = st.sidebar.date_input('split date', datetime.date(2021,6,1), min_value=datetime.date(2021,2,1), max_value=datetime.date.today())

    df['Date'] =  pd.to_datetime(df['Date'])

    dict_states={'TT': 'Total', 'WB': 'West Bengal', 'DL': 'Delhi', 'KL': 'Kerala', 'PB': 'Punjab', 'AP':'Andhra Pradesh', 
                'TN': 'Tamil Nadu', 'KA': 'Karnataka', 'JK': 'Jammu and Kashmir', 'UP': 'Uttar Pradesh', 'MP': 'Madhya Pradesh', 
                'MH': 'Maharashtra', 'BR': 'Bihar', 'HR': 'Haryana', 'OR': 'Orissa', 'RJ': 'Rajasthan', 'GJ': 'Gujarat', 
                'HP': 'Himachal Pradesh', 'AS': 'Assam', 'TG': 'Telangana', 'JH': 'Jharkhand', 'ML': 'Meghalaya', 
                'UT': 'Uttarakhand', 'CH': 'Chandigarh', 'CT': 'Chhattisgarh', 'LA': 'Lakshadweep', 'TR': 'Tripura', 
                'PY': 'Pondicherry', 'GA': 'Goa', 'AR': 'Arunachal Pradesh', 'DN': 'Dadra and Nagar Haveli', 
                'NL': 'Nagaland', 'SK':'Sikkim', 'AN': 'Andaman and Nicobar Islands', 'MN': 'Manipur', 'MZ': 'Mizoram', 
                'LD': 'Lakshadweep'}

    df['Year'] = df['Date'].dt.strftime('%Y')
    df['Month'] = df['Date'].dt.strftime('%m')
    df['Month']=pd.to_numeric(df['Month'])
    df['Day'] = df['Date'].dt.strftime('%d')

    df.dropna(inplace=True)

    df = df.replace({'State':dict_states})
    df.Confirmed = df.Confirmed.astype(int)
    df.Recovered = df.Recovered.astype(int)
    df.Deceased = df.Deceased.astype(int)
    df.Tested = df.Tested.astype(int)

    df_india = df.loc[df['State'] == 'Total']

    df_india_non_indexed=df_india.copy()

    df_india = df_india.set_index('Date')

    confirmed_india = df_india['Confirmed']
    recovered_india = df_india['Recovered']
    deceased_india = df_india['Deceased']
    tested_india = df_india['Tested']

    confirmed_india.plot()
    recovered_india.plot()
    deceased_india.plot()
    tested_india.plot()
    plt.legend()

    fig = px.line(df_india_non_indexed, x='Date', y='Confirmed', title='Confirmed with Slider')

    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=4, label="4m", step="month", stepmode="backward"),
                dict(count=8, label="8m", step="month", stepmode="backward"),
                dict(count=12, label="12m", step="month", stepmode="backward"),
                dict(step="all")
            ])
        )
    )
    st.plotly_chart(fig, use_container_width=True)

    def apply_prophet(df, split_date, isSeasonality):
        
        train=df[(df['ds'] <= split_date)]
        test=df[(df['ds'] > split_date)]

        cur_periods = test.shape[0]
        
        model = Prophet(interval_width=0.95, yearly_seasonality = isSeasonality)
        model.fit(train)
        model.params
        
        future = model.make_future_dataframe(periods=cur_periods)
        future.tail()
        
        forecast = model.predict(future)
        
        return model, forecast



    df_india_2021 = df_india[(df_india.index.get_level_values(0)) >= '2021-01-01']


    df_india_2021_prophet = df_india_2021.reset_index()[['Date','Confirmed']].rename({'Date':'ds','Confirmed':'y'}, axis='columns')
    split_f = datetime.datetime.strptime(str(split), '%Y-%m-%d')

    model, forecast = apply_prophet(df_india_2021_prophet, str(split), True)
    forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()

    mpl_fig = plt.figure()
    df_india_2021_prophet['ds']=pd.to_datetime(df_india_2021_prophet['ds'])
    plt.plot(pd.concat([df_india_2021_prophet[(df_india_2021_prophet.ds <= split_f)].set_index('ds')['y'],
                        forecast.set_index('ds')['yhat']],axis=1))

    st.write("Prediction from {}".format(str(split)))
    st.plotly_chart(model.plot(forecast), use_container_width=True)
    
    # st.write("Prediction Dataframe plot {}".format(str(split)))
    # st.plotly_chart(mpl_fig, use_container_width=True)
