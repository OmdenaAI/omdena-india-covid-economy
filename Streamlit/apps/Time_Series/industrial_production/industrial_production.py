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
    # best_model_order = joblib.load("apps/Time_Series/industrial_production/models/industrial production.sav")
    forcast = best_model_order.predict(n_periods=12, return_conf_int=False)
    
    
    future_dates = [dataset.index[-1]+ DateOffset(months = x)for x in range(0,12)]
    future_dates_df = pd.DataFrame(forcast,index=future_dates[0:])
    future_dataset = pd.concat([dataset,future_dates_df],axis='columns')

    future_dataset.columns = ['Actual','Forcast']
    
    fig = px.line(x = future_dataset.index, y = future_dataset['Actual'],title="Production rate forecast from the selected date")
    fig.add_scatter(x=future_dataset.index, y = future_dataset['Forcast'])
    fig.update_xaxes(
        rangeslider_visible=True,
        )
    fig.update_xaxes(title='Date')
    fig.update_yaxes(title='Rate')
    st.plotly_chart(fig, use_container_width=True)


def maini():
    st.write('Industrial Production Rate Forecast')
    st.markdown('This page allows you to check trends on Industrial production rate over the years in India.')
    
    st.sidebar.header("Date:")
    split = st.sidebar.date_input('split date', datetime.date(2021,1,1), min_value=datetime.date(2016,4,1), max_value=datetime.date(2021,1,1))

    industrial_production = pd.read_excel('apps/Time_Series/industrial_production/India Industrial Production.xlsx')

    for i in range(len(industrial_production['Release Date'])):
        industrial_production['Release Date'].iloc[i] = industrial_production['Release Date'].iloc[i].split(' (')[0]
        
    industrial_production['Release Date'] = pd.to_datetime(industrial_production['Release Date'])
    industrial_production.rename(columns = {"Release Date": "Date"},inplace = True)
    industrial_production.Date = pd.to_datetime(industrial_production.Date)
    industrial_production.sort_values(by=['Date'],ascending=True,inplace=True)
    industrial_production.set_index('Date',inplace = True)

    model_forcast_plot(industrial_production, "Actual", split)
