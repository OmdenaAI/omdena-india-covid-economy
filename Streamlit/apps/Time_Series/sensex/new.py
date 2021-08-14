import datetime
import warnings

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

warnings.filterwarnings('ignore')

from apps.Time_Series.sensex.oil import oil
from fbprophet import Prophet
from fbprophet.plot import add_changepoints_to_plot, plot_plotly


def analyse(data):
    fig = px.line(data,x='Date', y=['Close','Open','High','Low'])
    fig.update_xaxes(rangeslider_visible=True, title='Date')
    fig.update_yaxes(title='Price')
    st.plotly_chart(fig)

def predict(data, split_f):
    close_data = data[['Date','Close']]
    close_data = close_data.set_index('Date')
    m = Prophet(weekly_seasonality=False,yearly_seasonality=False)
    m.add_seasonality('self_define_cycle',period=8,fourier_order=8,mode='additive')

    data = data[['Date', 'Close']]
    data = data.rename(columns={'Date':'ds','Close':'y'})

    train=data[(data.ds <= split_f)]
    test=close_data[(close_data.index.get_level_values(0) >= split_f)]

    # train_data, test_data = data[:int(len(data)*0.9)], close_data[int(len(data)*0.9):]
    m.fit(train)

    pred = m.make_future_dataframe(periods=365)
    predictions = m.predict(pred)
    fig = plot_plotly(m, predictions)
    fig.update_xaxes(title='Date')
    fig.update_yaxes(title='Price')
    st.plotly_chart(fig)


def sensex(split):
    split_f = datetime.datetime.strptime(str(split), '%Y-%m-%d')
    st.header('BSE Sensex Analysis and Forecasting')
    sensex = pd.read_csv('apps/Time_Series/sensex/BSE_sensex.csv', sep=', ')
    sensex['Date'] = pd.to_datetime(sensex['Date'])
    st.markdown('Plotting raw data')
    analyse(sensex)

    st.markdown('Plotting Forecasted Data')
    predict(sensex, split_f)

def nifty(split):
    split_f = datetime.datetime.strptime(str(split), '%Y-%m-%d')
    st.header('NSE Nifty Analysis and Forecasting')
    nifty = pd.read_csv('apps/Time_Series/sensex/Nifty.csv')
    nifty['Date'] = pd.to_datetime(nifty['Date'])
    st.markdown('Plotting raw data')
    analyse(nifty)

    st.markdown('Plotting Forecasted Data')
    predict(nifty, split_f)

def new():
    st.title('Stock Market Forecasting')
    st.markdown('Due to the COVID-19, there were a lot of changes in the economy. Changes that had never occurred before. This page is meant to predict the state of the economy in the future in the perspective of the stock market')
    st.sidebar.header('Data:')
    choice = st.sidebar.selectbox('Choice:', ('BSE Sensex','NSE Nifty', 'Oil Exchange'))
    st.sidebar.header("Date:")
    split = st.sidebar.date_input('split date', datetime.date(2021,5,31), min_value=datetime.date(2016,1,31), max_value=datetime.date.today())
    if (choice == 'BSE Sensex'):
        sensex(split)
    elif(choice == 'NSE Nifty'):
        nifty(split)
    elif(choice == 'Oil Exchange'):
        oil(split)


