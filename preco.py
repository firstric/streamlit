import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

spx = pd.read_csv('./data/선행지수07_23.csv')
market = pd.read_csv('./data/유가증권07_2302.csv')

market.columns = ['Date','KOSPI', '거래량','거래대금','거래량(시외포)', '거래대금(시외포)', '시총', 'KOSDAQ', '거래량', '거래대금']
spx.columns = ['Date', 'SPX']

kospi = market[['Date', 'KOSPI']]
kosdaq = market[['Date', 'KOSDAQ']]

kospi['Date'] = pd.to_datetime(kospi['Date'], format='%Y-%m-%d')
kosdaq['Date'] = pd.to_datetime(kosdaq['Date'], format='%Y-%m-%d')
spx['Date'] = pd.to_datetime(spx['Date'], format='%Y-%m')

kospi.set_index('Date', inplace=True)
kospi = kospi.resample(rule='MS').first()

kosdaq.set_index('Date', inplace=True)
kosdaq = kosdaq.resample(rule='MS').first()

kospi.reset_index(inplace=True)
kosdaq.reset_index(inplace=True)

merge_data = pd.merge(spx, kospi, on='Date')
merge_data = pd.merge(merge_data, kosdaq, on='Date')

merge_data['KOSPI'] = merge_data['KOSPI'].str.replace(',','')
merge_data['KOSDAQ'] = merge_data['KOSDAQ'].str.replace(',','')

merge_data['SPX'] = merge_data['SPX'].astype(float)
merge_data['KOSPI'] = merge_data['KOSPI'].astype(float)
merge_data['KOSDAQ'] = merge_data['KOSDAQ'].astype(float)

fig, ax = plt.subplots(2,1)
ax[0].plot(merge_data['Date'], merge_data['SPX'], color = 'red', alpha = 0.5)

ax[0].set_ylabel('SPX', color = 'red', rotation = 0)
ax[0].set_ylim(90, 103)
ax_kospi = ax[0].twinx()
ax_kospi.plot(merge_data['Date'], merge_data['KOSPI'], color = 'green', alpha = 0.5)

ax_kospi.set_ylabel('KOSPI', color = 'green', rotation = 0)
ax_kospi.set_ylim(1000, 3600)

ax[1].plot(merge_data['Date'], merge_data['SPX'], color = 'red', alpha = 0.5)

ax[1].set_ylabel('SPX', color = 'red', rotation = 0)
ax[1].set_ylim(90, 103)
ax_kosdaq = ax[1].twinx()
ax_kosdaq.plot(merge_data['Date'], merge_data['KOSDAQ'], color = 'blue', alpha = 0.5)

ax_kosdaq.set_ylabel('KOSDAQ', color = 'blue', rotation = 0)
ax_kosdaq.set_ylim(300, 1100)
plt.show()

st.write('## 선행지수순환변동치 - KOSPI, KOSDAQ')
st.pyplot(fig)
st.write('SPX=선행지수순환변동치, KOSPI=KOSPI지수, KOSDAQ=KOSDAQ지수')

st.write('통계데이터(2007.02 ~ 2023.02)')
merge_data

