import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
st.sidebar.header("Pilih Dataset")
dataset_option = st.sidebar.selectbox("Pilih Dataset", ["Daily", "Hourly"])

# Load dataset
if dataset_option == "Daily":
    df = pd.read_csv('../data/day.csv')
elif dataset_option == "Hourly":
    df = pd.read_csv('../data/hour.csv')

df['dteday'] = pd.to_datetime(df['dteday'])

# Mapping untuk musim dan cuaca
season_mapping = {1: 'Musim Semi', 2: 'Musim Panas', 3: 'Musim Gugur', 4: 'Musim Dingin'}
weather_mapping = {1: 'Cerah', 2: 'Berawan', 3: 'Hujan', 4: 'Hujan Deras'}

df['season'] = df['season'].map(season_mapping)
df['weathersit'] = df['weathersit'].map(weather_mapping)

df['dteday'] = pd.to_datetime(df['dteday'], errors='coerce')
# Ekstrak tahun dan bulan
df['yr'] = df['dteday'].dt.year
df['mnth'] = df['dteday'].dt.month

st.title('📊 Dashboard Analisis Peminjaman Sepeda')

# **Pertanyaan 1: Pengaruh Cuaca terhadap Peminjaman Sepeda**
st.subheader('☀️ Pengaruh Cuaca terhadap Peminjaman Sepeda')
st.markdown("""
Cuaca memiliki peran penting dalam jumlah peminjaman sepeda. Berdasarkan data yang dianalisis:

- **Saat cuaca cerah atau sedikit berawan, jumlah peminjaman meningkat signifikan.**
- **Peminjaman paling sedikit terjadi saat hujan deras, kemungkinan karena kondisi jalan yang basah dan kurang nyaman untuk bersepeda.**
""")

weather_data = df.groupby('weathersit')['cnt'].mean().reset_index()
weather_data.rename(columns={'cnt': 'rata_peminjaman'}, inplace=True)

fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x='weathersit', y='rata_peminjaman', data=weather_data, ci=None, ax=ax)
ax.set_xlabel('Cuaca')
ax.set_ylabel('Rata-rata Jumlah Peminjaman')
ax.set_title('Peminjaman Sepeda Berdasarkan Cuaca')
st.pyplot(fig)

# **Pertanyaan 2: Pola Peminjaman Sepeda Berdasarkan Musim**
st.subheader('🌤️ Pola Peminjaman Sepeda Berdasarkan Musim')
st.markdown("""
Musim juga memengaruhi jumlah peminjaman sepeda:

- **Peminjaman sepeda paling banyak terjadi di Musim Gugur, kemungkinan karena cuaca lebih nyaman.**
- **Musim Semi memiliki tingkat peminjaman paling rendah, kemungkinan karena cuaca masih tidak menentu.**
- **Musim Panas memiliki jumlah peminjaman tinggi, tetapi sedikit lebih rendah dibandingkan Musim Gugur.**
""")

season_data = df.groupby('season')['cnt'].mean().reset_index()
season_data.rename(columns={'cnt': 'rata_peminjaman'}, inplace=True)

fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x='season', y='rata_peminjaman', data=season_data, ci=None, ax=ax)
ax.set_xlabel('Musim')
ax.set_ylabel('Rata-rata Jumlah Peminjaman')
ax.set_title('Peminjaman Sepeda Berdasarkan Musim')
st.pyplot(fig)

st.subheader('📈 Tren Peminjaman Sepeda per Musim')

# Pilih tahun untuk melihat tren
year_options = df['yr'].unique()
selected_year = st.selectbox('Pilih Tahun', year_options)

df_selected_year = df[df['yr'] == selected_year]

fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(data=df_selected_year, x='dteday', y='cnt', hue='season', palette='coolwarm', linewidth=2.5)
ax.set_xlabel('Tanggal')
ax.set_ylabel('Jumlah Peminjaman')
ax.set_title(f'Tren Peminjaman Sepeda Berdasarkan Musim ({selected_year})')
st.pyplot(fig)

st.markdown("""
**Kesimpulan:**
- Cuaca dan musim sangat berpengaruh terhadap jumlah peminjaman sepeda.
- Pengaruh Cuaca terhadap Peminjaman Sepeda: Kondisi cuaca yang cerah (Clear) mendorong lebih banyak peminjaman sepeda.
Cuaca buruk seperti hujan atau salju (Light Rain/Snow dan Heavy Rain/Snow) menyebabkan penurunan peminjaman sepeda.
- Pengaruh Musim terhadap Peminjaman Sepeda: Peminjaman sepeda paling tinggi pada musim gugur (Fall), diikuti oleh musim panas (Summer).
Peminjaman cenderung lebih rendah di musim semi (Spring) dan paling sedikit di musim dingin (Winter). Dilihat dari grafik kedua dataset peningkatan peminjaman sepeda pada musim panas dan puncaknya ada di musim gugur, barulah kemudian mengalami penurunan pada musim dingin dan musim semi
""")