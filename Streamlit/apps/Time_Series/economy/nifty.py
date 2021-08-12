import streamlit as st
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

import warnings
warnings.filterwarnings('ignore')

import plotly.offline as pyo
from plotly.offline import init_notebook_mode,plot,iplot

from fbprophet import Prophet
from fbprophet.plot import plot_plotly, add_changepoints_to_plot
from plotly.offline import iplot, init_notebook_mode


st.title('Stock Market Forecasting')

st.sidebar.header('Data')

st.header('NSE Nifty Analysis and Forecasting')
nifty = pd.read_csv('./nifty.csv')
nifty['Date'] = pd.to_datetime(nifty['Date'])
st.markdown('Plotting raw data')

fig = px.line(nifty,x='Date', y=['Close','Open','High','Low'])
fig.update_xaxes(rangeslider_visible=True, title='Date')
fig.update_yaxes(title='Price')
st.plotly_chart(fig)

st.markdown('Plotting Forecasted Data')
close_data = nifty[['Date','Close']]
close_data = close_data.set_index('Date')
m = Prophet(weekly_seasonality=False,yearly_seasonality=False)
m.add_seasonality('self_define_cycle',period=8,fourier_order=8,mode='additive')

data = nifty[['Date', 'Close']]
data = data.rename(columns={'Date':'ds','Close':'y'})

train_data, test_data = data[:int(len(data)*0.9)], close_data[int(len(data)*0.9):]
m.fit(train_data)

pred = m.make_future_dataframe(periods=365)
predictions = m.predict(pred)
fig = plot_plotly(m, predictions)
fig.update_xaxes(title='Date')
fig.update_yaxes(title='Price')
st.plotly_chart(fig)
