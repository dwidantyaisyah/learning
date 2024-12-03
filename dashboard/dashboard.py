import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Judul Dashboard
st.title("Proyek Analisis Data: Bike Sharing Dataset")

# Load dataset
uploaded_file = st.file_uploader("Upload Your Dataset", type=["csv", "xlsx"])
if uploaded_file is not None:
    # Load data berdasarkan jenis file
    if uploaded_file.name.endswith('.csv'):
        data = pd.read_csv(uploaded_file)
    else:
        data = pd.read_excel(uploaded_file)

    # Pastikan kolom tanggal dalam format datetime
    date_column = st.selectbox("Pilih Kolom Tanggal", data.columns)
    data[date_column] = pd.to_datetime(data[date_column])

    # Sidebar Filters
    st.sidebar.header("Filter")

    # Date Filter
    min_date = data[date_column].min()
    max_date = data[date_column].max()
    date_range = st.sidebar.date_input(
        "Pilih Rentang Tanggal",
        [min_date, max_date]
    )

    # Category Filter
    category_column = st.selectbox("Pilih Kolom Kategori", data.select_dtypes(include=['object', 'category']).columns)
    selected_categories = st.sidebar.multiselect(
        "Pilih Kategori",
        options=data[category_column].unique(),
        default=data[category_column].unique()
    )

    # Terapkan filter
    filtered_data = data[
        (data[date_column] >= pd.to_datetime(date_range[0])) &
        (data[date_column] <= pd.to_datetime(date_range[1])) &
        (data[category_column].isin(selected_categories))
    ]

    # Tampilkan data yang telah difilter
    st.write(f"Data yang Difilter ({len(filtered_data)} baris):")
    st.dataframe(filtered_data)

    # Visualisasi
    st.header("Visualisasi")

    # Line Chart
    numerical_columns = filtered_data.select_dtypes(include=['float64', 'int64']).columns
    if len(numerical_columns) > 0:
        line_chart_column = st.selectbox("Pilih Kolom untuk Grafik Garis", numerical_columns)

        plt.figure(figsize=(10, 5))
        plt.plot(filtered_data[date_column], filtered_data[line_chart_column], label=line_chart_column, color='blue')
        plt.xlabel("Tanggal")
        plt.ylabel(line_chart_column)
        plt.title(f"{line_chart_column} Seiring Waktu")
        plt.legend()
        st.pyplot(plt)
    else:
        st.warning("Tidak ada kolom numerik yang tersedia untuk grafik garis.")

    # Bar Chart
    st.header("Grafik Batang Kategori")
    bar_chart_data = filtered_data.groupby(category_column).size().reset_index(name='counts')
    
    if not bar_chart_data.empty:
        plt.figure(figsize=(8, 5))
        sns.barplot(data=bar_chart_data, x=category_column, y='counts', palette='viridis')
        plt.title(f"Jumlah berdasarkan {category_column}")
        plt.xlabel(category_column)
        plt.ylabel("Jumlah")
        plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
        st.pyplot(plt)
    else:
        st.warning("Tidak ada data untuk grafik batang.")

    # Correlation Heatmap
    st.header("Peta Panas Korelasi")
    corr = filtered_data.select_dtypes(include=['float64', 'int64']).corr()
    
    if not corr.empty:
        plt.figure(figsize=(10, 8))
        sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
        plt.title("Matriks Korelasi")
        st.pyplot(plt)
    else:
        st.warning("Tidak ada data numerik untuk matriks korelasi.")

else:
    st.info("Silakan unggah dataset untuk memulai.")
