#!/usr/bin/env python
# coding: utf-8

# > - **Total vaccines administered, people vaccinated once and fully vaccinated on a daily basis since 2021-01-15, however on 18th July is not available**: https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/country_data/India.csv (Our World in Data)
# > - **Daily vaccinations entry available since 2021-01-15 globally**: https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.csv (Our World in Data)
# > - **India's state-wise data about vaccinations for total vaccines administered, people vaccinated once and fully vaccinated on a daily basis since 2021-01-15 in CSV**: http://api.covid19india.org/csv/latest/vaccine_doses_statewise_v2.csv

import pandas as pd
import plotly.express as px

pd.options.display.max_columns = 100
# Dataset-2 on Global-wide countries
# > - Importing data from same resouces for extracting 'daily vaccinations' metric:
# > - From the below global vaccination data, rows have been filtered for India specific rows

# Pre-processing steps of the dataset
gh_raw_global_csv_url = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.csv'

vaccinations_global = pd.read_csv(gh_raw_global_csv_url)
print(vaccinations_global.head())

# vaccinations_global[vaccinations_global.iso_code == 'IND'][vaccinations_global.isna().any(axis=1)].fillna(0)
vaccinations_india_wise = vaccinations_global[vaccinations_global.iso_code == 'IND']
print(vaccinations_india_wise.head())

daily_vaccines_india_df = vaccinations_india_wise[['date', 'daily_vaccinations', 'location']]
print(daily_vaccines_india_df)

"""
Replacing NaNs with zero
"""
daily_vaccines_india_df = daily_vaccines_india_df.fillna(0)
daily_vaccines_india_df

# Save the pre-processed data to below named CSV:
daily_vaccines_india_df.to_csv('../datasets/daily_vaccines_india.csv', index=False)

print(daily_vaccines_india_df.info())

daily_vaccines_india_df['date'] = pd.to_datetime(daily_vaccines_india_df['date'])
"""
Extracting day, month and year from 'date' into new variables/columns respectively:
Note: DatetimeIndex() doesn't convert date object type to datetime data type
"""
daily_vaccines_india_df['day'] = pd.DatetimeIndex(daily_vaccines_india_df.date).day
daily_vaccines_india_df['month'] = pd.DatetimeIndex(daily_vaccines_india_df.date).month
daily_vaccines_india_df['year'] = pd.DatetimeIndex(daily_vaccines_india_df.date).year

# Confirm the above new columns have been created
print(daily_vaccines_india_df.head())

# Below statement helps to know how many total daily vaccinations were given every month:
daily_vaccines_india_monthly_df = daily_vaccines_india_df.groupby('month').agg({'daily_vaccinations': 'sum'})
daily_vaccines_india_monthly_df = daily_vaccines_india_monthly_df.reset_index()
print(daily_vaccines_india_monthly_df.head())

# Below graph is to visually show the flow of the progress of daily vaccinations every month India-wide:
# **Insights from this graph**:
# > - January to April there were growth in the daily vaccinations
# > - From April-May it was reduced
# > - From May-June there was growth
# > - From June, slight reduction
fig = px.line(daily_vaccines_india_monthly_df, 
              x='month', 
              y='daily_vaccinations', 
              title='Visual flow of Daily Vaccinations (in Millions) every month since Jan 2021')
fig.show()
