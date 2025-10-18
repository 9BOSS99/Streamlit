import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------------
# Налаштування сторінки
# ---------------------------------------
st.set_page_config(
    page_title="Інтерактивний дашборд судових справ",
    page_icon="⚖️",
    layout="wide"
)

st.title("⚖️ Інтерактивний дашборд судових справ України")
st.markdown("Аналіз даних судових рішень за регіонами, статтями та роками.")

# ---------------------------------------
# Завантаження CSV
# ---------------------------------------
uploaded_file = st.file_uploader(
    "📂 Завантаж CSV із реєстру судових рішень",
    type=["csv"]
)

if uploaded_file:
    # Читання CSV
    df = pd.read_csv(uploaded_file, parse_dates=["date"])
    
    # Перевірка колонок
    required_cols = {"region", "article", "category", "date"}
    if not required_cols.issubset(df.columns):
        st.error(f"CSV повинен містити колонки: {', '.join(required_cols)}")
        st.stop()

    # ---------------------------------------
    # Бічна панель із фільтрами
    # ---------------------------------------
    st.sidebar.header("🔍 Фільтри")
    regions = st.sidebar.multiselect(
        "Регіон:",
        options=sorted(df["region"].unique()),
        default=None
    )

    articles = st.sidebar.multiselect(
        "Стаття:",
        options=sorted(df["article"].unique()),
        default=None
    )

    date_range = st.sidebar.date_input(
        "Період:",
        [df["date"].min(), df["date"].max()]
    )

    # ---------------------------------------
    # Фільтрація
    # ---------------------------------------
    filtered = df.copy()

    if regions:
        filtered = filtered[filtered["region"].isin(regions)]
    if articles:
        filtered = filtered[filtered["article"].isin(articles)]
    if len(date_range) == 2:
        start, end = pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1])
        filtered = filtered[(filtered["date"] >= start) & (filtered["date"] <= end)]

    st.markdown("### 📋 Відфільтровані дані")
    st.dataframe(filtered, use_container_width=True)

    # ---------------------------------------
    # Діаграма кількості справ за категоріями
    # ---------------------------------------
    st.markdown("### 📊 Кількість справ за категоріями")

    cat_count = (
        filtered["category"]
        .value_counts()
        .reset_index()
        .rename(columns={"index": "Категорія", "category": "Кількість"})
    )

    fig_bar = px.bar(
        cat_count,
        x="Категорія",
        y="Кількість",
        color="Категорія",
        text_auto=True,
        title="Розподіл справ за категоріями"
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    # ---------------------------------------
    # Аналіз тенденцій по роках
    # ---------------------------------------
    st.markdown("### 📈 Тенденції по роках")

    filtered["year"] = filtered["date"].dt.year
    yearly = filtered.groupby("year").size().reset_index(name="Кількість справ")

    fig_line = px.line(
        yearly,
        x="year",
        y="Кількість справ",
        markers=True,
        title="Динаміка кількості судових справ по роках"
    )
    st.plotly_chart(fig_line, use_container_width=True)

    st.success("✅ Аналіз завершено!")
else:
    st.info("Будь ласка, завантаж CSV-файл для початку аналізу.")
