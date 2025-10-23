import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------------
# 🔹 Налаштування сторінки
# -------------------------------
st.set_page_config(
    page_title="Інтерактивний дашборд судових справ",
    page_icon="⚖️",
    layout="wide"
)

st.title("⚖️ Інтерактивний дашборд судових справ")
st.write("Аналіз даних із реєстру судових рішень України")

# -------------------------------
# 🔹 Завантаження CSV
# -------------------------------
st.sidebar.header("1️⃣ Завантаження даних")

uploaded_file = st.sidebar.file_uploader("Завантаж CSV-файл", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Перевірка мінімальних потрібних колонок
    required_columns = {"Регіон", "Стаття", "Категорія", "Дата"}
    if not required_columns.issubset(df.columns):
        st.error(f"CSV повинен містити колонки: {', '.join(required_columns)}")
    else:
        # -------------------------------
        # 🔹 Обробка даних
        # -------------------------------
        df["Дата"] = pd.to_datetime(df["Дата"], errors="coerce")
        df["Рік"] = df["Дата"].dt.year

        # -------------------------------
        # 🔹 Фільтри
        # -------------------------------
        st.sidebar.header("2️⃣ Фільтри")

        regions = df["Регіон"].dropna().unique()
        articles = df["Стаття"].dropna().unique()
        years = sorted(df["Рік"].dropna().unique())

        selected_region = st.sidebar.multiselect("Оберіть регіон(и)", regions, default=regions[:3])
        selected_article = st.sidebar.multiselect("Оберіть статтю(ї)", articles, default=articles[:3])
        selected_year = st.sidebar.slider("Оберіть діапазон років", int(min(years)), int(max(years)), (int(min(years)), int(max(years))))

        filtered_df = df[
            (df["Регіон"].isin(selected_region)) &
            (df["Стаття"].isin(selected_article)) &
            (df["Рік"] >= selected_year[0]) &
            (df["Рік"] <= selected_year[1])
        ]

        st.subheader("📊 Відфільтровані дані")
        st.dataframe(filtered_df)

        # -------------------------------
        # 🔹 Діаграма кількості справ за категоріями
        # -------------------------------
        st.subheader("📈 Кількість справ за категоріями")

        category_counts = filtered_df["Категорія"].value_counts()

        fig1, ax1 = plt.subplots()
        ax1.bar(category_counts.index, category_counts.values)
        ax1.set_xlabel("Категорія")
        ax1.set_ylabel("Кількість справ")
        ax1.set_title("Кількість справ за категоріями")
        plt.xticks(rotation=45)
        st.pyplot(fig1)

        # -------------------------------
        # 🔹 Аналіз тенденцій по роках
        # -------------------------------
        st.subheader("📅 Тенденції по роках")

        yearly_counts = filtered_df.groupby("Рік").size()

        fig2, ax2 = plt.subplots()
        ax2.plot(yearly_counts.index, yearly_counts.values, marker='o')
        ax2.set_xlabel("Рік")
        ax2.set_ylabel("Кількість справ")
        ax2.set_title("Динаміка кількості справ по роках")
        st.pyplot(fig2)

else:
    st.info("⬅️ Будь ласка, завантаж CSV-файл для початку аналізу.")
