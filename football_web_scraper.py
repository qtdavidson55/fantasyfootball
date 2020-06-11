from requests import get
import pandas as pd
from bs4 import BeautifulSoup


year = input('What season? Note: Input a season between 1999 and 2019: ')
year = int(year)

url = f'https://www.pro-football-reference.com/years/{year}/fantasy.htm'

defColumnSettings = {
    'axis': 1,
    'inplace': True
}

response = get(url)
soup = BeautifulSoup(response.content, 'html.parser')
table = soup.find('table', {'id': 'fantasy'})

df = pd.read_html(str(table))[0]
df.columns = df.columns.droplevel(level = 0)
df.drop(['FantPt', 'DKPt', 'FDPt', '2PM', '2PP', 'Rk'], **defColumnSettings)
df = df[df['FantPos'] != 'FantPos']
df.set_index(['Player', 'FantPos', 'Tm'], inplace=True)
df.fillna(0, inplace=True)
df = df.astype('float64')
df.reset_index()
df.to_csv(f'datasets/fantasy_{year}.csv')
