import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------------------
# Налаштування сторінки
# ---------------------------------------
st.set_page_config(
    page_title="Інтерактивний дашборд судових справ",
    page_icon="⚖️",
    layout="wide"
)

st.title("⚖️ Інтерактивний дашборд судових справ України")
st.markdown("Аналіз судових рішень за регіоном, статтею та роками.")

# ---------------------------------------
# Завантаження CSV
# ---------------------------------------
uploaded_file = st.file_uploader("📂 Завантаж CSV із судовими справами", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file, parse_dates=["date"])
    
    # Перевірка потрібних колонок
    required = {"region", "article", "category", "date"}
    if not required.issubset(df.columns):
        st.error(f"CSV має містити колонки: {', '.join(required)}")
        st.stop()

    # ---------------------------------------
    # Фільтри
    # ---------------------------------------
    st.sidebar.header("🔍 Фільтри")

    regions = st.sidebar.multiselect("Регіон", df["region"].unique())
    articles = st.sidebar.multiselect("Стаття", df["article"].unique())
    date_range = st.sidebar.date_input(
        "Період",
        [df["date"].min(), df["date"].max()]
    )

    # ---------------------------------------
    # Фільтрація даних
    # ---------------------------------------
    filtered = df.copy()
    if regions:
        filtered = filtered[filtered["region"].isin(regions)]
    if articles:
        filtered = filtered[filtered["article"].isin(articles)]
    if len(date_range) == 2:
        start, end = pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1])
        filtered = filtered[(filtered["date"] >= start) & (filtered["date"] <= end)]

    st.markdown("### 📋 Відфільтровані справи")
    st.dataframe(filtered, use_container_width=True)

    # ---------------------------------------
    # Діаграма кількості справ за категоріями
    # ---------------------------------------
    st.markdown("### 📊 Кількість справ за категоріями")

    cat_counts = filtered["category"].value_counts()

    fig1, ax1 = plt.subplots()
    cat_counts.plot(kind="bar", ax=ax1)
    ax1.set_xlabel("Категорія")
    ax1.set_ylabel("Кількість справ")
    ax1.set_title("Розподіл справ за категоріями")
    st.pyplot(fig1)

    # ---------------------------------------
    # Тенденції по роках
    # ---------------------------------------
    st.markdown("### 📈 Тенденції по роках")

    filtered["year"] = filtered["date"].dt.year
    year_counts = filtered["year"].value_counts().sort_index()

    fig2, ax2 = plt.subplots()
    year_counts.plot(kind="line", marker="o", ax=ax2)
    ax2.set_xlabel("Рік")
    ax2.set_ylabel("Кількість справ")
    ax2.set_title("Динаміка кількості судових справ по роках")
    st.pyplot(fig2)

    st.success("✅ Аналіз завершено!")
else:
    st.info("Будь ласка, завантаж CSV-файл для початку аналізу.")
