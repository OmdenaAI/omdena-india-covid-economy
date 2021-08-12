import matplotlib.pyplot as plt
import streamlit as st

import plotly
import plotly.express as px
import plotly.graph_objects as go
plt.rcParams['figure.figsize']=17,8
import cufflinks as cf
import plotly.offline as pyo
from plotly.offline import init_notebook_mode,plot,iplot

import datetime
import pandas as pd
from fbprophet import Prophet

from fbprophet.plot import plot_plotly
import plotly.offline as py

def mainv():
    st.title('Vaccination details Forecasting')
    st.markdown('This page allows you to check forecast of vaccinatoin doses, vaccinated rate from the selected date.')
    st.markdown('Ever since the Covid19 pandemic, vaccination has been observed to provide good immunity towards the virus, to check the forecast select a date.')
    
    st.sidebar.header('Data:')
    choice = st.sidebar.selectbox('Choice:', ('Total Vaccinations','People Vaccinated', 'Fully Vaccinated'))

    st.sidebar.header("Date:")
    split = st.sidebar.date_input('split date', datetime.date(2021,5,8), min_value=datetime.date(2021,1,1), max_value=datetime.date.today())

    df = pd.read_csv('https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/country_data/India.csv',parse_dates=['date'])
    df.drop(['location','source_url'],axis=1,inplace=True)
    df['month'] = df['date'].dt.month
    
    Confirmed = df[['date','total_vaccinations']]
    Confirmed1 = df[['date','people_vaccinated']]
    Confirmed2 = df[['date','people_fully_vaccinated']]

    Confirmed1.columns = ['ds','y']
    Confirmed2.columns = ['ds','y']
    Confirmed.columns = ['ds','y']

    split_f = datetime.datetime.strptime(str(split), '%Y-%m-%d')

    train1 = Confirmed1[Confirmed1['ds'] < split_f]
    test1 = Confirmed1[Confirmed1['ds'] >= split_f]
    train2 = Confirmed2[Confirmed2['ds'] < split_f]
    test2 = Confirmed2[Confirmed2['ds'] >= split_f]
    train = Confirmed[Confirmed['ds'] < split_f]
    test = Confirmed[Confirmed['ds'] >= split_f]

    m1 = Prophet(interval_width=0.9,daily_seasonality=True,seasonality_mode='additive')
    m2 = Prophet(interval_width=0.9,daily_seasonality=True)
    m = Prophet(interval_width=0.9,daily_seasonality=True,seasonality_mode='additive')

    m.fit(train)
    m1.fit(train1)
    m2.fit(train2)

    future1 = m1.make_future_dataframe(periods=12)
    future2 = m2.make_future_dataframe(periods=12)
    future = m.make_future_dataframe(periods=12)

    forecast1 = m1.predict(future1)
    forecast2 = m2.predict(future2)
    forecast = m.predict(future)

    confirmed_forecast_plot = m.plot(forecast)
    confirmed_forecast1_plot = m1.plot(forecast1)
    confirmed_forecast2_plot = m2.plot(forecast2)

    if choice == "Total Vaccinations":
        fig = plot_plotly(m, forecast)
        st.write("Forecast on total_vaccinations from {}".format(str(split)))
        st.plotly_chart(fig, use_container_width=True)

    elif choice == "People Vaccinated":
        st.write("Forecast on people_vaccinated from {}".format(str(split)))
        fig1 = plot_plotly(m1, forecast1)
        st.plotly_chart(fig1, use_container_width=True)

    elif choice == "Fully Vaccinated":
        st.write("Forecast on people_fully_vaccinated from {}".format(str(split)))
        fig2 = plot_plotly(m2, forecast2)
        st.plotly_chart(fig2, use_container_width=True)