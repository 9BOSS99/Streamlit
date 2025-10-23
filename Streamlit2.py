# Streamlit2.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Дашборд судових справ", layout="wide")
st.title("Інтерактивний дашборд судових справ")

# --- 1. Завантаження CSV з GitHub (публічне посилання) ---
CSV_URL = "https://raw.githubusercontent.com/your_user/your_repo/main/court_cases.csv"
df = pd.read_csv(CSV_URL, parse_dates=['Дата'])

# --- 2. Фільтри ---
регіони = st.sidebar.multiselect("Оберіть регіон", options=df['Регіон'].unique(), default=df['Регіон'].unique())
статті = st.sidebar.multiselect("Оберіть статтю", options=df['Стаття'].unique(), default=df['Стаття'].unique())
дата = st.sidebar.date_input("Оберіть дату (початок та кінець)", [df['Дата'].min(), df['Дата'].max()])

filtered = df[
    (df['Регіон'].isin(регіони)) &
    (df['Стаття'].isin(статті)) &
    (df['Дата'].between(pd.to_datetime(date[0]), pd.to_datetime(date[1])))
]

st.write(f"Кількість справ після фільтрації: {len(filtered)}")

# --- 3. Діаграма кількості справ за категоріями ---
st.subheader("Кількість справ за статтями")
category_counts = filtered['Стаття'].value_counts()
fig, ax = plt.subplots()
category_counts.plot(kind='bar', ax=ax, color='skyblue')
ax.set_xlabel("Стаття")
ax.set_ylabel("Кількість справ")
st.pyplot(fig)

# --- 4. Аналіз тенденцій по роках ---
st.subheader("Тенденції по роках")
filtered['Рік'] = filtered['Дата'].dt.year
year_counts = filtered.groupby('Рік').size()
fig2, ax2 = plt.subplots()
year_counts.plot(kind='line', marker='o', ax=ax2)
ax2.set_xlabel("Рік")
ax2.set_ylabel("Кількість справ")
st.pyplot(fig2)
