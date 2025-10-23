import streamlit as st
import pandas as pd
import plotly.express as px
from io import StringIO

st.set_page_config(page_title="Судові справи: Дашборд", layout="wide")
st.title("📊 Інтерактивний дашборд судових справ")

# Автоматично створюємо приклад CSV
csv_data = """
region,article,category,date
Львівська область,185,Кримінальна,2021-03-15
Київська область,190,Цивільна,2022-06-20
Одеська область,185,Кримінальна,2023-01-10
Львівська область,191,Адміністративна,2021-11-05
Київська область,185,Кримінальна,2022-02-28
Одеська область,190,Цивільна,2023-07-12
Львівська область,191,Адміністративна,2024-04-18
Київська область,185,Кримінальна,2024-09-30
Одеська область,191,Адміністративна,2025-01-22
"""

df = pd.read_csv(StringIO(csv_data), parse_dates=["date"])

# Фільтри
st.sidebar.header("🔍 Фільтри")
region = st.sidebar.multiselect("Регіон", options=df["region"].unique())
article = st.sidebar.multiselect("Стаття", options=df["article"].unique())
date_range = st.sidebar.date_input("Діапазон дат", [df["date"].min(), df["date"].max()])

# Застосування фільтрів
filtered_df = df.copy()
if region:
    filtered_df = filtered_df[filtered_df["region"].isin(region)]
if article:
    filtered_df = filtered_df[filtered_df["article"].isin(article)]
filtered_df = filtered_df[
    (filtered_df["date"] >= pd.to_datetime(date_range[0])) &
    (filtered_df["date"] <= pd.to_datetime(date_range[1]))
]

st.subheader("📂 Відібрані дані")
st.dataframe(filtered_df, use_container_width=True)

# Діаграма кількості справ за категоріями
st.subheader("📈 Кількість справ за категоріями")
category_counts = filtered_df["category"].value_counts().reset_index()
category_counts.columns = ["category", "count"]
fig_cat = px.bar(category_counts, x="category", y="count", color="category", title="Справи за категоріями")
st.plotly_chart(fig_cat, use_container_width=True)

# Аналіз тенденцій по роках
st.subheader("📊 Тенденції по роках")
filtered_df["year"] = filtered_df["date"].dt.year
yearly_trend = filtered_df.groupby("year").size().reset_index(name="cases")
fig_year = px.line(yearly_trend, x="year", y="cases", markers=True, title="Кількість справ по роках")
st.plotly_chart(fig_year, use_container_width=True)
