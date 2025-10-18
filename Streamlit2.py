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
st.markdown("Аналіз судових рішень за регіонами, статтями та роками.")

# ---------------------------------------
# Завантаження CSV
# ---------------------------------------
uploaded_file = st.file_uploader("📂 Завантаж CSV із судових справ", type=["csv"])

if uploaded_file:
    # Читання CSV через pandas
    df = pd.read_csv(uploaded_file, parse_dates=["date"])
    
    # Перевірка, чи є необхідні колонки
    required_cols = {"region", "article", "category", "date"}
    if not required_cols.issubset(df.columns):
        st.error(f"Файл має містити колонки: {', '.join(required_cols)}")
        st.stop()

    # ---------------------------------------
    # Бічна панель із фільтрами
    # ---------------------------------------
    st.sidebar.header("🔍 Фільтри")

    regions = st.sidebar.multiselect(
        "Оберіть регіон(и):",
        options=sorted(df["region"].unique()),
        default=None
    )

    articles = st.sidebar.multiselect(
        "Оберіть статтю(ї):",
        options=sorted(df["article"].unique()),
        default=None
    )

    date_range = st.sidebar.date_input(
        "Період розгляду справ:",
        [df["date"].min(), df["date"].max()]
    )

    # ---------------------------------------
    # Фільтрація даних через pandas
    # ---------------------------------------
    filtered = df.copy()

    if regions:
        filtered = filtered[filtered["region"].isin(regions)]
    if articles:
        filtered = filtered[filtered["article"].isin(articles)]
    if len(date_range) == 2:
        start, end = pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1])
        filtered = filtered[(filtered["date"] >= start) & (filtered["date"] <= end)]

    # ---------------------------------------
    # Таблиця з даними
    # ---------------------------------------
    st.markdown("### 📋 Відфільтровані судові справи")
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
    # Аналіз тенденцій по роках
    # ---------------------------------------
    st.markdown("### 📈 Тенденції кількості справ по роках")

    filtered["year"] = filtered["date"].dt.year
    year_counts = filtered["year"].value_counts().sort_index()

    fig2, ax2 = plt.subplots()
    year_counts.plot(kind="line", marker="o", ax=ax2)
    ax2.set_xlabel("Рік")
    ax2.set_ylabel("Кількість справ")
    ax2.set_title("Динаміка кількості судових справ по роках")
    st.pyplot(fig2)

    st.success("✅ Аналіз виконано успішно!")
else:
    st.info("Будь ласка, завантаж CSV-файл для початку роботи.")
