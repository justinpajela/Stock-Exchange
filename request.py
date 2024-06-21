import requests
import pandas as pd
import matplotlib.pyplot as plt
import pandas as pd
import requests
from psycopg2.extras import execute_batch
def request():
    API_KEY = 'W8QWBSMDIAE5X4SA'
    symbol = 'IBM'  
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}'
    r = requests.get(url)
    data = r.json()
    df = pd.DataFrame(data['Time Series (Daily)']).T
    df.index = pd.to_datetime(df.index)
    # Rename the columns explicitly to ensure correct mapping

    df = df.rename(columns={
        '1. open': 'Open', 
        '2. high': 'High', 
        '3. low': 'Low', 
        '4. close': 'Close', 
        '5. volume': 'Volume'
    })

    # Convert columns to float (except for 'Volume' which should be int)
    for column in ['Open', 'High', 'Low', 'Close']:
        df[column] = df[column].astype(float)

    # Volume is often represented as an integer
    df['Volume'] = df['Volume'].astype(int)
    print(df)
    records = [
        (date.strftime('%Y-%m-%d'), row['Open'], row['High'], row['Low'], row['Close'], row['Volume'], symbol)
        for date, row in df.iterrows()
    ]


    # Database connection details
    #conn = psycopg2.connect(dbname='stock_prices', user='justinp', password='', host='localhost')
    #cur = conn.cursor()

    # Insert data into the database
    '''
    execute_batch(cur, """
    INSERT INTO stock_prices (date, open, high, low, close, volume, symbol) 
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (date) DO NOTHING;
    """, records)

    conn.commit()
    cur.close()
    conn.close()
    ''' 
    print(df)
    plt.plot(df.index, df['Close'], label='Daily Close Price')
    plt.title('Daily Close Price')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.show()
#request()