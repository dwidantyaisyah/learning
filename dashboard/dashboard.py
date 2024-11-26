# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import csv
import streamlit as st
from datetime import datetime, timedelta

import pandas as pd

# Gathering Data
day_df = pd.read_csv("day.csv")
hour_df = pd.read_csv("hour.csv")

# Tampilkan informasi dataset
print("Dataset day.csv berhasil dimuat:")
print(day_df.head())
print("\nDataset hour.csv berhasil dimuat:")
print(hour_df.head())

# Periksa struktur dataset
print("\nStruktur Dataset day.csv:")
print(day_df.info())
print("\nStruktur Dataset hour.csv:")
print(hour_df.info())

# Periksa missing values
print("\nMissing values di day.csv:")
print(day_df.isnull().sum())
print("\nMissing values di hour.csv:")
print(hour_df.isnull().sum())

# Periksa duplikasi
print("\nJumlah duplikat di day.csv:", day_df.duplicated().sum())
print("Jumlah duplikat di hour.csv:", hour_df.duplicated().sum())

# Statistik deskriptif
print("\nStatistik deskriptif day.csv:")
print(day_df.describe())
print("\nStatistik deskriptif hour.csv:")
print(hour_df.describe())
 # Cleaning Data
# Konversi kolom 'dteday' ke datetime
day_df['dteday'] = pd.to_datetime(day_df['dteday'])
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

# Mapping kategori cuaca
weather_map = {1: 'Cerah', 2: 'Berkabut', 3: 'Salju', 4: 'Hujan'}
day_df['weathersit'] = day_df['weathersit'].map(weather_map)
hour_df['weathersit'] = hour_df['weathersit'].map(weather_map)

# Tangani missing values dengan rata-rata (jika ada)
day_df.fillna(day_df.mean(), inplace=True)
hour_df.fillna(hour_df.mean(), inplace=True)

# Hapus duplikasi
day_df.drop_duplicates(inplace=True)
hour_df.drop_duplicates(inplace=True)

# Validasi hasil cleaning
print("\nDataset day.csv setelah cleaning:")
print(day_df.info())
print(day_df.head())
print("\nDataset hour.csv setelah cleaning:")
print(hour_df.info())
print(hour_df.head())

import matplotlib.pyplot as plt
import seaborn as sns

# Hitung rata-rata jumlah penyewaan berdasarkan kondisi cuaca
mean_cnt_by_weather = day_df.groupby('weathersit')['cnt'].mean().sort_values(ascending=False)

# Normalisasi warna untuk visualisasi
norm = plt.Normalize(mean_cnt_by_weather.min(), mean_cnt_by_weather.max())
colors = plt.cm.viridis(norm(mean_cnt_by_weather.values))

# Visualisasi
plt.figure(figsize=(10, 6))
sns.barplot(x=mean_cnt_by_weather.index, y=mean_cnt_by_weather.values, palette=colors)
plt.title('Rata-rata Jumlah Penyewaan Sepeda berdasarkan Kondisi Cuaca')
plt.xlabel('Kondisi Cuaca')
plt.ylabel('Rata-rata Jumlah Penyewaan')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

# Hitung rata-rata jumlah penyewaan berdasarkan musim
mean_cnt_by_season = day_df.groupby('season')['cnt'].mean().sort_values(ascending=False)

# Visualisasi
plt.figure(figsize=(10, 6))
sns.barplot(x=mean_cnt_by_season.index, y=mean_cnt_by_season.values, palette="coolwarm")
plt.title('Rata-rata Jumlah Penyewaan Sepeda berdasarkan Musim')
plt.xlabel('Musim')
plt.ylabel('Rata-rata Jumlah Penyewaan')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

# Rata-rata jumlah penyewaan per jam
mean_cnt_by_hour = hour_df.groupby('hr')['cnt'].mean()

# Visualisasi
plt.figure(figsize=(12, 6))
sns.lineplot(x=mean_cnt_by_hour.index, y=mean_cnt_by_hour.values, marker='o', color='b')
plt.title('Rata-rata Penyewaan Sepeda Berdasarkan Jam')
plt.xlabel('Jam')
plt.ylabel('Rata-rata Jumlah Penyewaan')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.xticks(range(0, 24, 1))
plt.show()

# Scatter plot penyewaan vs suhu
plt.figure(figsize=(10, 6))
sns.scatterplot(x=day_df['temp'], y=day_df['cnt'], hue=day_df['season'], palette='coolwarm', s=100)
plt.title('Hubungan Suhu dengan Penyewaan Sepeda')
plt.xlabel('Suhu (normalized)')
plt.ylabel('Jumlah Penyewaan')
plt.grid(axis='both', linestyle='--', alpha=0.7)
plt.legend(title='Musim')
plt.show()

# Hitung rata-rata penyewaan untuk pengguna kasual dan terdaftar
mean_casual_registered = hour_df[['casual', 'registered']].mean()

# Visualisasi
plt.figure(figsize=(8, 5))
sns.barplot(x=mean_casual_registered.index, y=mean_casual_registered.values, palette='viridis')
plt.title('Rata-rata Penyewaan Pengguna Kasual dan Terdaftar')
plt.xlabel('Jenis Pengguna')
plt.ylabel('Rata-rata Jumlah Penyewaan')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

# Visualisasi boxplot penyewaan berdasarkan hari
plt.figure(figsize=(12, 6))
sns.boxplot(x=day_df['weekday'], y=day_df['cnt'], palette='muted')
plt.title('Distribusi Penyewaan Sepeda Berdasarkan Hari')
plt.xlabel('Hari dalam Seminggu (0: Minggu, 6: Sabtu)')
plt.ylabel('Jumlah Penyewaan')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

# Gabungkan kedua dataset berdasarkan tanggal
merged_data = pd.merge(hour_df, day_df, on='dteday', suffixes=('_hour', '_day'))

# Periksa hasil penggabungan
print("\nHasil Gabungan Dataset:")
print(merged_data.info())
print(merged_data.head())

# Hitung total penyewaan kasual dan terdaftar berdasarkan musim
user_cnt_by_season = merged_data.groupby('season_day')[['casual', 'registered']].sum()

# Visualisasi
user_cnt_by_season.plot(kind='bar', stacked=True, figsize=(10, 6), colormap='coolwarm')
plt.title('Distribusi Penyewaan Kasual dan Terdaftar Berdasarkan Musim')
plt.xlabel('Musim')
plt.ylabel('Jumlah Penyewaan')
plt.legend(title='Jenis Pengguna')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

# Tambahkan kolom bulan ke dataset day_df
day_df['month'] = day_df['dteday'].dt.month

# Hitung total jumlah penyewaan per bulan
monthly_rentals = day_df.groupby('month')['cnt'].sum()

# Visualisasi
plt.figure(figsize=(10, 6))
sns.lineplot(x=monthly_rentals.index, y=monthly_rentals.values, marker='o', color='g')
plt.title('Jumlah Penyewaan Sepeda Berdasarkan Bulan')
plt.xlabel('Bulan')
plt.ylabel('Total Penyewaan')
plt.xticks(range(1, 13))
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

# Buat pivot table dari hour_df untuk jam dan hari
heatmap_data = hour_df.pivot_table(index='hr', columns='weekday', values='cnt', aggfunc='mean')

# Visualisasi Heatmap
plt.figure(figsize=(12, 8))
sns.heatmap(heatmap_data, cmap='YlGnBu', annot=True, fmt=".1f", linewidths=.5)
plt.title('Rata-rata Penyewaan Sepeda Berdasarkan Jam dan Hari')
plt.xlabel('Hari dalam Seminggu (0: Minggu, 6: Sabtu)')
plt.ylabel('Jam')
plt.show()

# Hitung korelasi antara variabel numerik di day_df
correlation_matrix = day_df.corr()

# Visualisasi Heatmap Korelasi
plt.figure(figsize=(12, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5)
plt.title('Korelasi antara Variabel Numerik')
plt.show()

# Hitung total penyewaan untuk hari kerja dan akhir pekan
rentals_by_workingday = day_df.groupby('workingday')['cnt'].sum()

# Visualisasi
plt.figure(figsize=(8, 5))
sns.barplot(x=rentals_by_workingday.index, y=rentals_by_workingday.values, palette='muted')
plt.title('Jumlah Penyewaan Sepeda: Hari Kerja vs Akhir Pekan')
plt.xlabel('Hari Kerja (0: Akhir Pekan, 1: Hari Kerja)')
plt.ylabel('Total Penyewaan')
plt.xticks(ticks=[0, 1], labels=['Akhir Pekan', 'Hari Kerja'])
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

#RFM ANALISYST
import pandas as pd
# Load data dari file day.csv
file_path = ('data/day.csv')  
df = pd.read_csv(file_path)
# Periksa data
print(df.head())

import pandas as pd

# Memuat data
file_path = ('data/day.csv') 
df = pd.read_csv(file_path)

# Pastikan kolom dteday dalam format datetime
if 'dteday' in df.columns:
    df['dteday'] = pd.to_datetime(df['dteday'])
else:
    raise ValueError("Kolom 'dteday' tidak ditemukan dalam dataset.")

# Menentukan tanggal referensi (snapshot_date)
snapshot_date = df['dteday'].max() + pd.Timedelta(days=1)

# Pastikan kolom yang digunakan ada di dataset
required_columns = ['season', 'temp', 'weathersit', 'workingday', 'cnt']
missing_columns = [col for col in required_columns if col not in df.columns]
if missing_columns:
    raise ValueError(f"Kolom berikut tidak ditemukan dalam dataset: {missing_columns}")

# Menambahkan kolom total penyewaan sebagai Monetary
df['total_rentals'] = df['cnt']  # Kolom cnt mewakili total penyewaan

# Menghitung RFM berdasarkan musim, suhu, cuaca, dan hari kerja
rfm_df = df.groupby(['season', 'temp', 'weathersit', 'workingday']).agg({
    'dteday': lambda x: (snapshot_date - x.max()).days,  # Recency
    'total_rentals': 'count',  # Frequency
    'cnt': 'sum'  # Monetary
}).reset_index()

# Mengubah nama kolom hasil agregasi
rfm_df.columns = ['season', 'temp', 'weathersit', 'workingday', 'recency', 'frequency', 'monetary']

# Pastikan kolom monetary adalah tipe data numerik
rfm_df['monetary'] = pd.to_numeric(rfm_df['monetary'], errors='coerce')

# Mengatasi potensi error dengan qcut
try:
    # Membagi nilai Recency, Frequency, Monetary ke dalam kuartil
    rfm_df['r_quartile'] = pd.qcut(rfm_df['recency'], 4, labels=[4, 3, 2, 1])  # Recency: 1 = baru
    rfm_df['f_quartile'] = pd.qcut(rfm_df['frequency'], 4, labels=[1, 2, 3, 4])  # Frequency: 4 = sering
    rfm_df['m_quartile'] = pd.qcut(rfm_df['monetary'], 4, labels=[1, 2, 3, 4])  # Monetary: 4 = banyak
except ValueError as e:
    print("Terjadi kesalahan pada qcut. Pastikan data cukup bervariasi untuk kuartil. Kesalahan:", e)
    rfm_df['r_quartile'] = pd.cut(rfm_df['recency'], 4, labels=[4, 3, 2, 1])
    rfm_df['f_quartile'] = pd.cut(rfm_df['frequency'], 4, labels=[1, 2, 3, 4])
    rfm_df['m_quartile'] = pd.cut(rfm_df['monetary'], 4, labels=[1, 2, 3, 4])

# Menggabungkan nilai RFM Score
rfm_df['RFMScore'] = rfm_df['r_quartile'].astype(str) + rfm_df['f_quartile'].astype(str) + rfm_df['m_quartile'].astype(str)

# Menampilkan hasil akhir
print(rfm_df[['season', 'temp', 'weathersit', 'workingday', 'recency', 'frequency', 'monetary', 'RFMScore']].head())

#HISTOGRAM BLOXPOT
import matplotlib.pyplot as plt
import seaborn as sns

# Visualisasi distribusi Monetary dengan Histogram
plt.figure(figsize=(10, 6))
sns.histplot(rfm_df['monetary'], bins=20, kde=True, color='blue')
plt.title('Distribusi Monetary (Total Penyewaan)', fontsize=16)
plt.xlabel('Monetary (Total Penyewaan)', fontsize=12)
plt.ylabel('Frekuensi', fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

# Visualisasi distribusi Monetary dengan Boxplot
plt.figure(figsize=(8, 5))
sns.boxplot(x=rfm_df['monetary'], color='cyan')
plt.title('Boxplot Monetary (Total Penyewaan)', fontsize=16)
plt.xlabel('Monetary (Total Penyewaan)', fontsize=12)
plt.grid(axis='x', linestyle='--', alpha=0.7)
plt.show()

#SCATERPLOT
import matplotlib.pyplot as plt
import seaborn as sns

# Visualisasi Scatter Plot RFM Segmen
plt.figure(figsize=(10, 6))
sns.scatterplot(x='recency', y='frequency', hue='RFMScore', data=rfm_df, palette='viridis', s=100, edgecolor='k', alpha=0.7)
plt.title('Distribusi Segmen RFM: Recency vs Frequency', fontsize=16)
plt.xlabel('Recency (Hari Terakhir Penyewaan)', fontsize=12)
plt.ylabel('Frequency (Jumlah Penyewaan)', fontsize=12)
plt.legend(title='RFM Score', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)
plt.show()

#HEATMAP
# Membuat tabel korelasi antara Recency, Frequency, dan Monetary
rfm_corr = rfm_df[['recency', 'frequency', 'monetary']].corr()

# Visualisasi Heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(rfm_corr, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
plt.title('Korelasi antara Recency, Frequency, dan Monetary', fontsize=16)
plt.show()

#RFM SCORE
import matplotlib.pyplot as plt
import seaborn as sns

# Visualisasi distribusi RFM Score dengan Histogram
plt.figure(figsize=(10, 6))
sns.histplot(rfm_df['RFMScore'], bins=10, kde=False, color='skyblue', discrete=True)
plt.title('Distribusi RFM Score', fontsize=16)
plt.xlabel('RFM Score', fontsize=12)
plt.ylabel('Frekuensi', fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

