import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import chardet

st.set_page_config(page_title="Дашборд судових справ", layout="wide")
st.title("📊 Інтерактивний дашборд судових справ")

# Завантаження CSV
uploaded_file = st.file_uploader("Завантажте CSV-файл із судовими справами", type="csv")

if uploaded_file is not None:
    # Визначення кодування
    raw_data = uploaded_file.read()
    encoding = chardet.detect(raw_data)["encoding"]
    uploaded_file.seek(0)
    
    # Зчитування CSV
    df = pd.read_csv(uploaded_file, encoding=encoding)
    
    st.subheader("Відображення даних")
    st.dataframe(df)

    # --- Фільтри ---
    region = st.selectbox("Оберіть регіон", ["Усі"] + sorted(df["Регіон"].unique()))
    article = st.selectbox("Оберіть статтю", ["Усі"] + sorted(df["Стаття"].unique()))
    
    filtered = df.copy()
    if region != "Усі":
        filtered = filtered[filtered["Регіон"] == region]
    if article != "Усі":
        filtered = filtered[filtered["Стаття"] == article]

    st.subheader("Відфільтровані дані")
    st.dataframe(filtered)

    # --- Графік: кількість справ за категоріями ---
    st.subheader("Кількість справ за категоріями")
    fig, ax = plt.subplots()
    filtered["Категорія"].value_counts().plot(kind="bar", ax=ax, color="skyblue")
    ax.set_xlabel("Категорія")
    ax.set_ylabel("Кількість справ")
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # --- Аналіз тенденцій по роках ---
    st.subheader("Тенденції по роках")
    filtered["Рік"] = pd.to_datetime(filtered["Дата"], errors="coerce").dt.year
    trend = filtered.groupby("Рік").size()
    fig2, ax2 = plt.subplots()
    trend.plot(kind="line", marker="o", ax=ax2)
    ax2.set_xlabel("Рік")
    ax2.set_ylabel("Кількість справ")
    st.pyplot(fig2)

