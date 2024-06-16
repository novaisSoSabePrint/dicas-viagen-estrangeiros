import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt

# Função para buscar cotações em tempo real
def get_exchange_rate(base_currency, target_currency):
    api_key = 'SUA_API_KEY'
    url = f'https://api.exchangerate-api.com/v4/latest/{base_currency}'
    response = requests.get(url)
    data = response.json()
    return data['rates'][target_currency]

# Função para buscar histórico de cotações
def get_historical_rates(base_currency, target_currency, days):
    api_key = 'SUA_API_KEY'
    url = f'https://api.exchangerate-api.com/v4/history/{base_currency}'
    response = requests.get(url)
    data = response.json()
    rates = data['rates']
    df = pd.DataFrame(rates).T[target_currency].tail(days)
    return df

st.title('Conversor de Moedas')

# Seção de conversão
st.header('Conversor')
base_currency = st.selectbox('Moeda de origem', ['USD', 'EUR', 'BRL'])
target_currency = st.selectbox('Moeda de destino', ['USD', 'EUR', 'BRL'])
amount = st.number_input('Valor', min_value=0.0, format="%.2f")
if st.button('Converter'):
    rate = get_exchange_rate(base_currency, target_currency)
    converted_amount = amount * rate
    st.write(f'{amount} {base_currency} = {converted_amount:.2f} {target_currency}')

# Seção de histórico
st.header('Histórico de Cotações')
days = st.selectbox('Período', [7, 30, 365])
if st.button('Mostrar Histórico'):
    df = get_historical_rates(base_currency, target_currency, days)
    st.line_chart(df)

# Seção de favoritos
st.header('Favoritos')
favorite_pairs = st.multiselect('Selecione seus pares favoritos', [('USD', 'EUR'), ('EUR', 'BRL'), ('USD', 'BRL')])
if favorite_pairs:
    st.write('Pares favoritos:')
    for pair in favorite_pairs:
        rate = get_exchange_rate(pair[0], pair[1])
        st.write(f'{pair[0]}/{pair[1]}: {rate:.2f}')

