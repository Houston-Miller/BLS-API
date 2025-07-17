import json
import requests
import pandas as pd
import matplotlib.pyplot as plt

#############################################################################################################
###  This will not work as a standalone python script as the 'dataset' dataframe is populated by Power BI ###
###      For a brief example outside of Power BI, uncomment line 56 and comment out line 57.              ###
#############################################################################################################

#assuming this is loaded into a PBI Python visual - the dataset variable is provided by Power BI
# dataset = pandas.DataFrame(BLSID, Config Name)
# dataset = dataset.drop_duplicates()

key_df=pd.read_csv('API_KEY.csv')
BLS_ENDPOINT = "https://api.bls.gov/publicAPI/v2/timeseries/data/"

#key_df.loc[key_df['API'] == 'bls', 'KEY'].item()
BLS_API_KEY = key_df.columns[0]
BLS_ENDPOINT = "https://api.bls.gov/publicAPI/v2/timeseries/data/"

def fetch_bls_series(series, **kwargs):
    """
    Pass in a list of BLS series IDs, Arguments can be provided as kwargs
        - startyear (4 digit year)
        - endyear (4 digit year)
        - catalog (True/False)
        - calculations (True/False)
        - annualaverage (True/False)
        - registrationKey (API key)       
    """

    if len(series) < 1 or len(series) > 50:
        raise ValueError("Series list must be between 1 and 50 series IDs")
    # create headers and payload POST request
    headers = {'Content-Type': 'application/json'}
    payload = {
        "seriesid": series,
        "registrationKey": BLS_API_KEY
    }
    # add kwargs to payload
    payload.update(kwargs)
    payload = json.dumps(payload)
    # make the request
    response = requests.post(BLS_ENDPOINT, data=payload, headers=headers)
    response.raise_for_status()

    result = response.json()
    if result.get('status') != 'REQUEST_SUCCEEDED':
        error_message = f"BLS API Error: Status - {result.get('status', 'UNKNOWN')}"
        if result.get('message'):
            error_message += f". Messages: {', '.join(result['message'])}"
        raise Exception(error_message)
    return result

#series = [CUURS12BSAF116,CUURS12BSAA,CUURS12BSAE,CUURS12BSAF1,CUURS12BSEFV,CUURS12BSAH3]
series = dataset['Series ID'].tolist()
json_data = fetch_bls_series(series, startyear='2017', endyear='2023')

try:
    #create a list to store individual dataframes
    dfs= []

    for series in json_data['Results']['series']:
        df_initial = pd.DataFrame(series)
        series_col = df_initial['seriesID'][0]

        for i in range(0, len(df_initial) - 1):
            df_row = pd.DataFrame(df_initial['data'][i])
            df_row['seriesID'] = series_col

            if 'code' not in str(df_row['footnotes']):
                df_row['footnotes'] = ''
            else:
                df_row['footnotes'] = str(df_row['footnotes']).split("'code': '", 1)[1][:1]

            # Append df_row to the list of dataframes
            dfs.append(df_row)

    # Concatenate all dataframes in the list into a single dataframe
    df = pd.concat(dfs, ignore_index=True)

    #save the dataframe to a CSV file
    #df.to_csv('bls_data.csv', index=False)

except Exception as e:
    json_data['status'] == 'REQUEST_NOT_PROCESSED'
    print('BLS API Error: Status - ', json_data['status'])
    print('Reason:', json_data['message'])
    print('Error:', str(e))

df['year'] = pd.to_numeric(df['year'])
df['value'] = pd.to_numeric(df['value'])
df['year-period'] = df['year'].astype(str) + '-' + df['period']

df_wide = df.pivot(index='year-period', columns='seriesID', values='value')

df_wide = df_wide.sort_index()

df_indexed = df_wide.apply(lambda x: (x / x.dropna().iloc[0]) * 100)

plt.figure(figsize=(15, 8))

df_indexed.plot(
    kind='line',
    ax=plt.gca()
)

plt.axhline(100, color='grey', linestyle='--', alpha=0.6)

plt.title('Relative Growth of BLS Series (Indexed to Start = 100)', fontsize=16)
plt.xlabel('Time Period (Year-Month)', fontsize=12)
plt.ylabel('Index (Start of Period = 100)', fontsize=12)

plt.grid(True, linestyle='--', alpha=0.6)

plt.legend(title='Series ID', bbox_to_anchor=(1.05, 1), loc='upper left')

plt.tight_layout()
plt.show()