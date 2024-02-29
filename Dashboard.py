import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style='dark')

st.title('Dashboard Penyewaan Sepeda')

awaldf = pd.read_csv("dataStreamlit/dataMerge.csv")
awaldfDay = pd.read_csv("dataStreamlit/dataDay.csv")

awaldf['dteday'] = pd.to_datetime(awaldf['dteday'])
awaldfDay['dteday'] = pd.to_datetime(awaldfDay['dteday'])

min_date = awaldf["dteday"].min()
max_date = awaldf["dteday"].max()


with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("gambar/sepeda.png")

    awaldfDay.info()
    type(max_date)
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

dfDay = awaldfDay[(awaldfDay["dteday"] >= str(start_date)) & 
                (awaldfDay["dteday"] <= str(end_date))]

df = awaldf[(awaldf["dteday"] >= str(start_date)) & 
                (awaldf["dteday"] <= str(end_date))]

# Membuat kolom baru untuk bulan
dfDay['month'] = dfDay['dteday'].dt.month

col1, col2, col3 = st.columns(3)
 
with col1:
    total_penyewaan = dfDay["cnt"].sum()
    st.metric("Total penyewaan", value=total_penyewaan)

with col2:
    total_casual = dfDay["casual"].sum()
    st.metric("Casual Riders", value=total_casual)

with col3:
    total_registered = dfDay["registered"].sum()
    st.metric("Registered Riders", value=total_registered) 

st.markdown("---")

# Lineplot Jumlah penyewaan sepeda setiap bulan
st.subheader('Jumlah penyewaan sepeda setiap bulan')

total = dfDay.groupby('month')['cnt'].sum()
casual = dfDay.groupby('month')['casual'].sum()
registered = dfDay.groupby('month')['registered'].sum()

plt.figure(figsize=(10, 6))
total.plot(kind='line', marker='o', color='g')
registered.plot(kind='line', marker='o', color='b')
casual.plot(kind='line', marker='o', color='r')
plt.xlabel('Bulan')
plt.ylabel('Jumlah Penyewaan')
plt.xticks(range(1, 13), ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Ags', 'Sep', 'Okt', 'Nov', 'Des'])
plt.grid(True)
plt.legend()
st.pyplot(plt)

#Lineplot Rata-rata penyewaan tiap bulan
st.subheader('Rata-rata penyewaan sepeda setiap bulan')

total = dfDay.groupby('month')['cnt'].mean()
casual = dfDay.groupby('month')['casual'].mean()
registered = dfDay.groupby('month')['registered'].mean()

plt.figure(figsize=(10, 6))
total.plot(kind='line', marker='o', color='g')
registered.plot(kind='line', marker='o', color='b')
casual.plot(kind='line', marker='o', color='r')
plt.xlabel('Bulan')
plt.ylabel('Jumlah Penyewaan')
plt.xticks(range(1, 13), ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Ags', 'Sep', 'Okt', 'Nov', 'Des'])
plt.grid(True)
plt.legend()
st.pyplot(plt)

# Barplot Total penyewa sepeda berdasarkan cuaca
st.subheader("Total penyewa berdasarkan cuaca")

grouped_data = dfDay.groupby('weathersit')[['casual', 'registered']].sum()
grouped_data = grouped_data.reindex(['Baik', 'Mendung', 'Buruk'])

plt.figure(figsize=(10, 6))
bar_width = 0.35
index = np.arange(len(grouped_data.index))

# Plot bar untuk masing-masing grup
bars_casual = plt.bar(index, grouped_data['casual'], bar_width, label='Casual', color = "r")
bars_registered = plt.bar(index, grouped_data['registered'], bar_width,  bottom=grouped_data['casual'] , label='Registered', color = "b")

plt.xlabel('Weather Situation')
plt.ylabel('Total Penyewaan')
plt.xticks(index, grouped_data.index)
plt.legend()
plt.grid(True)
plt.gca().get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))
for i, bar in enumerate(bars_registered):
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + grouped_data['casual'][i], grouped_data['casual'][i] + grouped_data['registered'][i], ha='center', va='bottom')
st.pyplot(plt)

# Barplot Rata-Rata Penyewaan Sepeda berdasarkan kondisi cuaca
st.subheader('Rata-Rata Penyewaan Sepeda berdasarkan Kondisi Cuaca')
col1, col2 = st.columns(2)
with col1:
    st.caption('Per Hari')
    data = df.groupby('weathersitHour')['cntHour'].mean().reset_index().sort_values("cntHour", ascending=False)
    palette = sns.color_palette("RdBu", 4)
    fig, ax = plt.subplots(figsize=(10, 6))
    barplot = sns.barplot(x='cntHour', y='weathersitHour', data=data, palette=palette, hue="cntHour", orient="h", legend=False)

    plt.title('Rata - Rata Penyewaan Sepeda per Jam berdasarkan Kondisi Cuaca')
    plt.xlabel('Rata - Rata Penyewaan')
    plt.ylabel('Kondisi Cuaca')

    for index, value in enumerate(data['cntHour']):
        barplot.text(value, index, round(value), ha='left', va='center')

    st.pyplot(fig)

with col2:
    st.caption('Per Jam')
    data = df.groupby('weathersitDay')['cntDay'].mean().reset_index().sort_values("cntDay", ascending=False)

    palette = sns.color_palette("RdBu", 4)[1:]

    plt.figure(figsize=(10, 6))
    barplot = sns.barplot(x='cntDay', y='weathersitDay', data=data, palette=palette, hue="cntDay", orient="h", legend=False)

    plt.title('Rata - Rata Penyewaan Sepeda per Hari berdasarkan Kondisi Cuaca')
    plt.xlabel('Rata - Rata Penyewaan')
    plt.ylabel('Kondisi Cuaca')
    for index, value in enumerate(data['cntDay']):
        barplot.text(value, index, round(value), ha='left', va='center')
    st.pyplot(plt)

#Membuat kluster peminjaman sepeda
st.subheader('Kluster peminjaman sepeda')

#Kluster kelembapan
st.caption('Kluster peminjaman sepeda berdasarkan kelembapan dan kategori cuaca (2011-2012)')
palette = {"Baik": "blue", "Mendung": "orange", "Buruk": "red"}
plt.figure(figsize=(10,6))
scatter = sns.scatterplot(x='humDay', y='cntDay', data=df, hue='weathersitDay', palette=palette, hue_order=["Baik", "Mendung", "Buruk"])
plt.xlabel("Kelembapan (%)")
plt.ylabel("Total Peminjaman Sepeda")
plt.title("Kluster peminjaman sepeda berdasarkan kelembapan dan kategori cuaca (2011-2012)")
maxCount = df['cntDay'].max()
maxHumidity = df.loc[df['cntDay'].idxmax()]['humDay']
plt.annotate(f'Max\nPenyewa: {maxCount}\nKelembapan: {maxHumidity:.2f}%',
             xy=(maxHumidity, maxCount),
             xytext=(maxHumidity - 25, maxCount - 500),
             arrowprops=dict(facecolor='black', shrink=0.05))

minCount = df['cntDay'].min()
minHumidity = df.loc[df['cntDay'].idxmin()]['humDay']
plt.annotate(f'Min\nPenyewa: {minCount}\nKelembapan: {minHumidity:.2f}%',
             xy=(minHumidity, minCount),
             xytext=(minHumidity - 25, minCount),
             arrowprops=dict(facecolor='black', shrink=0.05))

handles, labels = scatter.get_legend_handles_labels()
plt.legend(handles=handles, labels=["Baik", "Mendung", "Buruk"], title="Kategori Cuaca")

plt.tight_layout()
st.pyplot(plt)

#Kluster kecepatan angin
st.caption("Kluster peminjaman sepeda berdasarkan kecepatan angin dan kategori cuaca (2011-2012)")
plt.figure(figsize=(10,6))
sns.scatterplot(x='windspeedDay', y='cntDay', data=df, hue='weathersitDay', palette=palette, hue_order=["Baik", "Mendung", "Buruk"])
plt.xlabel("Kecepatan angin")
plt.ylabel("Total Peminjaman Sepeda")
plt.title("Kluster peminjaman sepeda berdasarkan kecepatan angin dan kategori cuaca (2011-2012)")

maxCount = df['cntDay'].max()
maxWindspeed = df.loc[df['cntDay'].idxmax()]['windspeedDay']
plt.annotate(f'Max\nPenyewa: {maxCount}\nKecepatan angin: {maxWindspeed:.2f}',
             xy=(maxWindspeed, maxCount),
             xytext=(maxWindspeed + 2, maxCount - 500),
             arrowprops=dict(facecolor='black', shrink=0.05))

minCount = df['cntDay'].min()
minWindspeed = df.loc[df['cntDay'].idxmin()]['windspeedDay']
plt.annotate(f'Min\nPenyewa: {minCount}\nKecepatan angin: {minWindspeed:.2f}',
             xy=(minWindspeed, minCount),
             xytext=(minWindspeed - 7, minCount),
             arrowprops=dict(facecolor='black', shrink=0.05))

plt.legend(title="Kategori Cuaca")
plt.tight_layout()
st.pyplot(plt)

#Kluster Suhu
st.caption("Kluster peminjaman sepeda berdasarkan suhu dan kategori cuaca (2011-2012)")
plt.figure(figsize=(10,6))
scatter = sns.scatterplot(x='tempDay', y='cntDay', data=df, hue='weathersitDay', palette=palette, hue_order=["Baik", "Mendung", "Buruk"])
plt.xlabel("Temperatur (C)")
plt.ylabel("Total Peminjaman Sepeda")
plt.title("Kluster peminjaman sepeda berdasarkan suhu dan kategori cuaca (2011-2012)")

maxCount = df['cntDay'].max()
maxTemp = df.loc[df['cntDay'].idxmax()]['tempDay']
plt.annotate(f'Max\nPenyewa: {maxCount}\nSuhu: {maxTemp:.2f} C',
             xy=(maxTemp, maxCount),
             xytext=(maxTemp + 2, maxCount - 500),
             arrowprops=dict(facecolor='black', shrink=0.05))

minCount = df['cntDay'].min()
minTemp = df.loc[df['cntDay'].idxmin()]['tempDay']
plt.annotate(f'Min\nPenyewa: {minCount}\nSuhu: {minTemp:.2f} C',
             xy=(minTemp, minCount),
             xytext=(minTemp + 3, minCount),
             arrowprops=dict(facecolor='black', shrink=0.05))

handles, labels = scatter.get_legend_handles_labels()
plt.legend(handles=handles, labels=["Baik", "Mendung", "Buruk"], title="Kategori Cuaca")

plt.legend(title="Kategori Cuaca")
plt.tight_layout()
st.pyplot(plt)

#Lineplot peminjaman sepeda per hari
st.subheader("Peminjaman Sepeda per Hari dari 2011 - 2012")
# Mencari tanggal mulai masing-masing musim tahun 2011
dingin = dfDay["dteday"][dfDay.index[dfDay['season'] == 'Dingin'].min()]
dinginText = dfDay["dteday"][dfDay.index[dfDay['season'] == 'Dingin'].min()+5]
semi = dfDay["dteday"][dfDay.index[dfDay['season'] == 'Semi'].min()]
semiText = dfDay["dteday"][dfDay.index[dfDay['season'] == 'Semi'].min()+5]
panas = dfDay["dteday"][dfDay.index[dfDay['season'] == 'Panas'].min()]
panasText = dfDay["dteday"][dfDay.index[dfDay['season'] == 'Panas'].min()+5]
gugur = dfDay["dteday"][dfDay.index[dfDay['season'] == 'Gugur'].min()]
gugurText = dfDay["dteday"][dfDay.index[dfDay['season'] == 'Gugur'].min()+5]

# Mencari tanggal mulai masing-masing musim tahun 2012
filtered_df = dfDay[dfDay['dteday'].dt.year >= 2012]

dingin2 = dfDay["dteday"][filtered_df.index[filtered_df['season'] == 'Dingin'].min()]
dingin2Text = dfDay["dteday"][filtered_df.index[filtered_df['season'] == 'Dingin'].min()+5]
semi2 = dfDay["dteday"][filtered_df.index[filtered_df['season'] == 'Semi'].min()]
semi2Text = dfDay["dteday"][filtered_df.index[filtered_df['season'] == 'Semi'].min()+5]
panas2 = dfDay["dteday"][filtered_df.index[filtered_df['season'] == 'Panas'].min()]
panas2Text = dfDay["dteday"][filtered_df.index[filtered_df['season'] == 'Panas'].min()+5]
gugur2 = dfDay["dteday"][filtered_df.index[filtered_df['season'] == 'Gugur'].min()]
gugur2Text = dfDay["dteday"][filtered_df.index[filtered_df['season'] == 'Gugur'].min()+5]

# Membuat line plot
dfDay['dteday'] = pd.to_datetime(dfDay['dteday'])
dfDay['bulan'] = dfDay['dteday'].dt.strftime('%B')

# Plotting
plt.figure(figsize=(16,6))

plt.plot(dfDay['dteday'], dfDay['cnt'], label='Semua Data')

plt.scatter(dfDay[dfDay["weathersit"] == "Normal"]['dteday'],
            dfDay[dfDay["weathersit"] == "Normal"]['cnt'],
            color='yellow', label='Cuaca Normal')

plt.scatter(dfDay[dfDay["weathersit"] == "Buruk"]['dteday'],
            dfDay[dfDay["weathersit"] == "Buruk"]['cnt'],
            color='red', label='Cuaca Buruk')

plt.axvline(x=dingin, color='gray', linestyle='--', label=None)
plt.axvline(x=semi, color='gray', linestyle='--', label=None)
plt.axvline(x=panas, color='gray', linestyle='--', label=None)
plt.axvline(x=gugur, color='gray', linestyle='--', label=None)
plt.text(dinginText, plt.ylim()[1], 'Mulai Musim Dingin', ha='left', va='top', rotation=90)
plt.text(semiText, plt.ylim()[1], 'Mulai Musim Semi', ha='left', va='top', rotation=90)
plt.text(panasText, plt.ylim()[1], 'Mulai Musim Panas', ha='left', va='top', rotation=90)
plt.text(gugurText, plt.ylim()[1], 'Mulai Musim Gugur', ha='left', va='top', rotation=90)

plt.axvline(x=dingin2, color='gray', linestyle='--', label=None)
plt.axvline(x=semi2, color='gray', linestyle='--', label=None)
plt.axvline(x=panas2, color='gray', linestyle='--', label=None)
plt.axvline(x=gugur2, color='gray', linestyle='--', label=None)
plt.text(dingin2Text, plt.ylim()[1], 'Mulai Musim Dingin', ha='left', va='top', rotation=90)
plt.text(semi2Text, plt.ylim()[0], 'Mulai Musim Semi', ha='left', va='bottom', rotation=90)
plt.text(panas2Text, plt.ylim()[0], 'Mulai Musim Panas', ha='left', va='bottom', rotation=90)
plt.text(gugur2Text, plt.ylim()[0], 'Mulai Musim Gugur', ha='left', va='bottom', rotation=90)

plt.title('Line Chart Peminjaman Sepeda per Hari dari 2011 - 2012')
plt.xlabel('Bulan')
plt.ylabel('Nilai')
plt.grid(True)
plt.xticks(rotation=45)
plt.legend(loc='upper right')

# Menampilkan plot menggunakan Streamlit
st.pyplot(plt)