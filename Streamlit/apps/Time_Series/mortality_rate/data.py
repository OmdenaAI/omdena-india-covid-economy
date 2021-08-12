import requests
import pandas as pd


def jsonToCsv(mydict):
    rows = []
    row=[]

    for state in mydict.keys():
        row.append(state)
        state_data = mydict[state]
        dates_data = state_data['dates']

        for date in dates_data.keys():
            if dates_data[date].get('delta') is None:
                continue;

            date_total_data = dates_data[date]['delta']
            nc = date_total_data.get('confirmed', None)
            nr = date_total_data.get('recovered', None)
            nd = date_total_data.get('deceased', None)
            nt = date_total_data.get('tested', None)

            row.append(date) 
            row.append(nc) 
            row.append(nr) 
            row.append(nd) 
            row.append(nt) 

            rows.append(row)

            row=[]
            row.append(state)

        row=[]


    df = pd.DataFrame(rows)
    df.columns = ['State', 'Date', 'Confirmed', 'Recovered', 'Deceased', 'Tested']
    df['Confirmed']=df['Confirmed'].astype('Int64')
    df['Recovered']=df['Recovered'].astype('Int64')
    df['Deceased']=df['Deceased'].astype('Int64')
    df['Tested']=df['Tested'].astype('Int64')
    
    return df