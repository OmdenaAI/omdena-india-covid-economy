import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st

plt.rcParams['figure.figsize']=17,8
import datetime

import joblib
import pandas as pd
from pandas.tseries.offsets import DateOffset
import pmdarima as pm

def model_forcast_plot(dataset_,columns_, split):
    split = datetime.datetime.strptime(str(split), '%Y-%m-%d')
    
    dataset = dataset_[columns_].copy()
    dataset = dataset_[(dataset_.index.get_level_values(0) <= split)]
    dataset = dataset[columns_]

    best_model_order = pm.auto_arima(dataset, 
                                start_p=1, start_q=1, max_p=3, max_q=5, 
                                start_P=0, start_Q=0, max_P=3, max_Q=3, m=11, 
                                seasonal=True, trace=True, 
                                d=1, D=1, 
                                error_action='warn', 
                                suppress_warnings=True, 
                                random_state = 3).fit(dataset)
    # best_model_order = joblib.load("apps/Time_Series/gdp/models/GDP.sav")
    forcast = best_model_order.predict(n_periods=12, return_conf_int=False)
    
    
    future_dates = [dataset.index[-1]+ DateOffset(months = x)for x in range(0,12)]
    future_dates_df = pd.DataFrame(forcast,index=future_dates[0:])
    future_dataset = pd.concat([dataset,future_dates_df],axis='columns')

    future_dataset.columns = ['Actual','Forcast']
    
    fig = px.line(x = future_dataset.index, y = future_dataset['Actual'],title="GDP forecast from the selected date")
    fig.add_scatter(x=future_dataset.index, y = future_dataset['Forcast'])
    fig.update_xaxes(
        rangeslider_visible=True,
        )
    fig.update_xaxes(title='Date')
    fig.update_yaxes(title='Rate')
    st.plotly_chart(fig, use_container_width=True)


def maing():
    st.write('GDP Forecast')
    st.markdown('This page allows you to check trends on Gross Domestic Product over the years in India.')
    
    st.sidebar.header("Date:")
    split = st.sidebar.date_input('split date', datetime.date(2021,1,1), min_value=datetime.date(1996,4,1), max_value=datetime.date.today())

    gdp = pd.read_csv('apps/Time_Series/gdp/GDP_Data.csv',parse_dates=['Date'])
    gdp.set_index('Date',inplace = True)
    gdp.index = pd.to_datetime(gdp.index)
    model_forcast_plot(gdp, "GDP",split)
