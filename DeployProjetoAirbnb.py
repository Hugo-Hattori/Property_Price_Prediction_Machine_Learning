import pandas as pd
import streamlit as st
import joblib


x_numericos = {'latitude': 0, 'longitude': 0, 'accommodates': 0, 'bathrooms': 0, 'bedrooms': 0, 'beds': 0, 'extra_people': 0,
               'minimum_nights': 0, 'ano': 0, 'mês': 0, 'n_amenities': 0, 'host_listings_count': 0}

x_tf = {'host_is_superhost': 0, 'instant_bookable': 0}

x_listas = {'property_type': ['Apartment', 'Bed and breakfast', 'Condominium', 'Guest suite', 'Guesthouse', 'Hostel', 'House', 'Loft', 'Outros', 'Serviced apartment'],
            'room_type': ['Entire home/apt', 'Hotel room', 'Private room', 'Shared room'],
            'cancellation_policy': ['flexible', 'moderate', 'strict', 'strict_14_with_grace_period']
            }

dict_aux = {}
for chave in x_listas:
    for valor in x_listas[chave]:
        dict_aux[f'{chave}_{valor}'] = 0

for item in x_numericos:
    if item == 'longitude' or item == 'latitude':
        valor = st.number_input(f'{item}', step=0.00001, value=0.0, format='%.5f') #o format aqui é parecido porém não igual ao utilizado no python normalmente
    elif item == 'extra_people':
        valor = st.number_input(f'{item}', step=0.01, value=0.0)
    else:
        valor = st.number_input(f'{item}', step=1, value=0)
    x_numericos[item] = valor
    
for item in x_tf:
    valor = st.selectbox(f'{item}', ('Sim', 'Não'))
    x_tf[item] = 1 if valor == 'Sim' else 0

for chave in x_listas:
    valor = st.selectbox(f'{chave}', x_listas[chave])
    dict_aux[f'{chave}_{valor}'] = 1

botao = st.button('Prever Valor do Imóvel')

if botao:
    dict_aux.update(x_numericos)
    dict_aux.update(x_tf)
    valores_x = pd.DataFrame(dict_aux, index=[0])

    dados = pd.read_csv('dados.csv')
    colunas = list(dados.columns)[1:-1]
    valores_x = valores_x[colunas]

    modelo = joblib.load('modelo.joblib')
    preco = modelo.predict(valores_x)
    st.write(preco[0])