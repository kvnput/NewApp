import pandas as pd  
import matplotlib.pyplot as plt  
import seaborn as sns  
import streamlit as st  
from babel.numbers import format_currency  

sns.set(style='whitegrid')

try:
    data_sepeda = pd.read_csv('dataset/day.csv')
except FileNotFoundError:
    st.error("Dataset tidak ditemukan. Pastikan file 'day.csv' ada di folder 'dataset'.")
    st.stop()

st.title('📊 Analisis Penggunaan Sepeda')

st.sidebar.header("Filter Data")
start_date = pd.to_datetime(st.sidebar.date_input("Tanggal Awal", pd.to_datetime(data_sepeda['dteday']).min()))
end_date = pd.to_datetime(st.sidebar.date_input("Tanggal Akhir", pd.to_datetime(data_sepeda['dteday']).max()))

data_sepeda['dteday'] = pd.to_datetime(data_sepeda['dteday'])

data_filtered = data_sepeda[(data_sepeda['dteday'] >= start_date) & (data_sepeda['dteday'] <= end_date)]

analisis_terpilih = st.selectbox(
    '🔍 Pilih Analisis:',
    ['Analisis Musiman', 'Dampak Kondisi Cuaca']
)

if analisis_terpilih == 'Analisis Musiman':
    st.subheader('🚴‍♂️ Pola Penggunaan Sepeda Berdasarkan Musim')

    fig, ax = plt.subplots(figsize=(14, 7))
    sns.barplot(x='season', y='cnt', data=data_filtered, hue='mnth', palette='Set2', ax=ax, ci=None)
    ax.set_title('Distribusi Penggunaan Sepeda per Musim dan Bulan', fontsize=14)
    ax.set_xlabel('Musim')
    ax.set_ylabel('Jumlah Penggunaan')
    st.pyplot(fig)

    fig, ax = plt.subplots(figsize=(14, 6))
    sns.barplot(x='weekday', y='cnt', data=data_filtered, palette='coolwarm', ax=ax, ci=None)
    ax.set_title('Penggunaan Sepeda Berdasarkan Hari dalam Seminggu', fontsize=14)
    ax.set_xlabel('Hari dalam Minggu')
    ax.set_ylabel('Jumlah Pengguna')
    st.pyplot(fig)

elif analisis_terpilih == 'Dampak Kondisi Cuaca':
    st.subheader('🌦️ Hubungan Penggunaan Sepeda dengan Cuaca')

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x='weathersit', y='cnt', data=data_filtered, palette='magma', ax=ax, ci=None)
    ax.set_title('Distribusi Penggunaan Sepeda per Kondisi Cuaca', fontsize=14)
    ax.set_xlabel('Kondisi Cuaca')
    ax.set_ylabel('Jumlah Pengguna')
    st.pyplot(fig)

    korelasi = data_filtered[['cnt', 'temp', 'atemp', 'hum', 'windspeed']].corr()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(korelasi, annot=True, cmap='viridis', fmt=".2f", ax=ax)
    ax.set_title('Matriks Korelasi Faktor Cuaca', fontsize=14)
    st.pyplot(fig)

st.sidebar.subheader("Debugging Info")
st.sidebar.write("Jumlah data setelah filter:", len(data_filtered))
