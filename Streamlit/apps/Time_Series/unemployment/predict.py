import matplotlib.pyplot as plt
import streamlit as st

import plotly
import plotly.express as px
import plotly.graph_objects as go
plt.rcParams['figure.figsize']=17,8
import cufflinks as cf

import datetime
import pandas as pd
#from fbprophet import Prophet

import pmdarima as pm

#from fbprophet.plot import plot_plotly
import plotly.offline as py

def mainu():
    st.title('Unemployment Rate Forecasting')
    st.markdown('This page allows you to check forecast of unemployment rate from the selected date.')
    st.markdown('Due to Covid19, unemployment has been a static result for all, which is the most downgraded result since 2015')
    st.sidebar.header("Date:")
    split = st.sidebar.date_input('split date', datetime.date(2021,5,31), min_value=datetime.date(2016,1,31), max_value=datetime.date.today())

    df = pd.read_csv('apps/Time_Series/unemployment/Unemployment_Rate_Monthly.csv',parse_dates=[' Date'])
    df['Date']=pd.to_datetime(df[' Date'])
    df.drop([' Date',' Frequency'],axis=1,inplace=True)
    df= df[df['Region'] == 'India']
    df=df.set_index('Date')

    split_f = datetime.datetime.strptime(str(split), '%Y-%m-%d')

    train=df[(df.index.get_level_values(0) <= split_f)]
    test=df[(df.index.get_level_values(0) >= split_f)]

    model = pm.auto_arima(df[' Estimated Unemployment Rate (%)'], 
                        m=12, seasonal=True,
                      start_p=0, start_q=0, max_order=4,error_action='ignore',  
                           suppress_warnings=True,
                      stepwise=True, trace=True)

    model.fit(train[' Estimated Unemployment Rate (%)'])

    forecast1=model.predict(n_periods=12, return_conf_int=True)
    forecast_range=pd.date_range(start=str(split), periods=12,freq='M')
    forecast1_df = pd.DataFrame(forecast1[0],index =forecast_range,columns=['Prediction'])

    mpl_fig = plt.figure()
    plt.plot(pd.concat([df[(df.index.get_level_values(0) <= split_f)][' Estimated Unemployment Rate (%)'],forecast1_df],axis=1))
    plt.xlabel('Date')
    plt.ylabel('Rate')
    st.write("Unemployment Rate Forecast from {}".format(str(split)))
    st.plotly_chart(mpl_fig, use_container_width=True)