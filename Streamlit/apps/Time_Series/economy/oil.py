import datetime
import itertools
import warnings

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import statsmodels.api as sm
import streamlit as st
from statsmodels.tsa.statespace.sarimax import SARIMAX

warnings.filterwarnings('ignore')

def analyse(data):
    st.dataframe(data.head())

    
    fig = px.line(data ,x='Date', y=['Close','Open','High','Low'])
    fig.update_xaxes(title='Date',rangeslider_visible=True)
    fig.update_yaxes(title='Price')
    st.plotly_chart(fig)

    fig = px.line(data ,x='Date', y=['Volume'], title="Volume")
    fig.update_xaxes(title='Date',rangeslider_visible=True)
    fig.update_yaxes(title='Volume')
    st.plotly_chart(fig)

def predict(data, split_f):

    data=data[(data.index.get_level_values(0) <= split_f)]
    p = d = q = range(0, 2)
    pdq = list(itertools.product(p, d, q))
    # parameter combinations for seasonal ARIMA
    seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]
    
    for param in pdq:
        for param_seasonal in seasonal_pdq:
            try:
                mod = sm.tsa.statespace.SARIMAX(data,
                                                order=param,
                                                seasonal_order=param_seasonal,
                                                enforce_stationarity=False,
                                                enforce_invertibility=False)
                results = mod.fit()
            except:
                continue
    
    mod = sm.tsa.statespace.SARIMAX(data,
                                order=(1, 1, 1),
                                seasonal_order=(1, 1, 0, 12),
                                enforce_stationarity=False,
                                enforce_invertibility=False)
    results = mod.fit()
    
    pred_uc = results.get_forecast(steps=10)
    pred_ci = pred_uc.conf_int()
    mpl_fig = plt.figure()
    ax = data.plot(label='observed', figsize=(14, 7))
    pred_uc.predicted_mean.plot(ax=ax, label='Forecast')
    ax.fill_between(pred_ci.index,
                    pred_ci.iloc[:, 0],
                    pred_ci.iloc[:, 1], color='k', alpha=.25)
    ax.set_xlabel('Date')
    ax.set_ylabel('Closing Price')
    plt.legend()
    # st.plotly_chart(mpl_fig, use_container_width=True)
    st.pyplot(plt)



def oil(split):
    split_f = datetime.datetime.strptime(str(split), '%Y-%m-%d')
    oil=pd.read_csv("apps/Time_Series/economy/Oil Prices.csv")
    oil['Date'] = pd.to_datetime(oil['Date'])
    analyse(oil)
    oil = oil.set_index('Date')
    oil = oil['Close'].resample('MS').mean()
    predict(oil, split_f)

