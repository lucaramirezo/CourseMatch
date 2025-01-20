import streamlit as st

# Tab: Recomendador de Cursos
def render_courses_tab(courses_data, model, recommend_courses_function):
    st.title("🔍 Recomendador de Cursos")
    st.write("Encuentra cursos basados en tus intereses y preferencias.")

    keyword = st.sidebar.text_input("**Palabra clave (ej.: Python, Machine Learning, JavaScript):**", value="")
    level = st.sidebar.selectbox("**Nivel del curso:**", options=["Todos"] + list(courses_data['Level'].unique()))
    rating_range = st.sidebar.slider("**Rango de calificación:**", min_value=0.0, max_value=5.0, value=(4.0, 5.0), step=0.1)
    platform = st.sidebar.selectbox("**Plataforma:**", options=["Todas"] + list(courses_data['Platform'].unique()))
    top_n = st.sidebar.number_input("**Número de recomendaciones:**", min_value=1, max_value=20, value=5)
    popularity_weight = st.sidebar.slider("**Peso de la popularidad:**", min_value=0.0, max_value=1.0, value=0.5)

    level = None if level == "Todos" else int(level)
    platform = None if platform == "Todas" else platform

    if st.sidebar.button("🔍 Obtener recomendaciones"):
        if not keyword.strip():
            st.error("Por favor, ingresa una palabra clave.")
        else:
            recommendations = recommend_courses_function(
                courses_data=courses_data,
                model=model,
                keyword=keyword,
                level=level,
                rating_range=rating_range,
                platform=platform,
                top_n=top_n,
                popularity_weight=popularity_weight
            )
            if isinstance(recommendations, str):
                st.warning(recommendations)
            else:
                st.markdown("### 📚 Cursos recomendados:")
                st.dataframe(recommendations)


# Tab: Tendencias Tecnológicas
def render_trends_tab(trends_2024, roles_2024, learning_methods_2024):
    st.title("📊 Tendencias Tecnológicas")
    st.write(
        "Explora las tendencias actuales en tecnologías, roles y métodos de aprendizaje "
        "según encuestas recientes. Descubre cursos relacionados con estas tendencias."
    )

    # Lenguajes en Auge y Declive
    st.subheader("Lenguajes en Auge y Declive")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Lenguajes en Auge")
        st.table(trends_2024[['Language', 'Growth']].head(5))
    with col2:
        st.markdown("### Lenguajes en Declive")
        st.table(trends_2024[['Language', 'Growth']].tail(5))

    # Roles emergentes
    st.subheader("Roles Emergentes y Habilidades Clave")
    st.dataframe(roles_2024[['DevType', 'Language', 'Growth']].head(20))

    # Métodos de aprendizaje
    st.subheader("Métodos de Aprendizaje Preferidos")
    st.table(learning_methods_2024[['Method', 'TotalFrequency']].head(10))
