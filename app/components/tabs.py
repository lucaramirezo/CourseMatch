import streamlit as st
import pandas as pd

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
def render_trends_tab(trends_2024, roles_2024, learning_methods_2024, courses_data, model, recommend_courses_function):
    # Introducción
    st.title("📊 Tendencias Tecnológicas")
    st.markdown(
        """
        Bienvenido a la sección de **Tendencias Tecnológicas**, basada en los datos de las encuestas anuales de 
        [Stack Overflow](https://insights.stackoverflow.com/survey). Aquí encontrarás:
        - Los lenguajes de programación y tecnologías más deseadas y en declive.
        - Roles emergentes y las habilidades clave asociadas.
        - Métodos de aprendizaje preferidos por la comunidad.

        **Enlaces a encuestas recientes**:
        - [Encuesta 2024](https://insights.stackoverflow.com/survey/2024)
        - [Encuesta 2023](https://insights.stackoverflow.com/survey/2023)
        - [Encuesta 2022](https://insights.stackoverflow.com/survey/2022)
        """
    )
    st.markdown("---")

    # Lenguajes en Auge y Declive
    st.subheader("📈 Lenguajes en Auge y Declive")
    st.write("Descubre los lenguajes más deseados o en declive según los datos más recientes.")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Lenguajes en Auge")
        st.table(format_dataframe_with_ranking(trends_2024, ['Language', 'Growth'], top_n=5))
    with col2:
        st.markdown("### Lenguajes en Declive")
        st.table(trends_2024[['Language', 'Growth']].tail(5))

    # Conexión con el recomendador: Selección de lenguaje
    selected_language = st.selectbox(
        "🔍 Selecciona un lenguaje para buscar cursos relacionados:",
        options=trends_2024['Language'].unique()
    )
    if st.button("Buscar cursos relacionados con este lenguaje"):
        recommendations = recommend_courses_function(
            courses_data=courses_data,
            model=model,
            keyword=selected_language,
            top_n=5
        )
        if isinstance(recommendations, str):
            st.warning("No se encontraron cursos relacionados.")
        else:
            st.markdown(f"### 📚 Cursos relacionados con **{selected_language}**:")
            st.dataframe(recommendations)

    st.markdown("---")

    # Roles Emergentes
    st.subheader("👩‍💻 Roles Emergentes y Habilidades Clave")
    st.write("Estos son los roles destacados y las habilidades asociadas.")
    st.dataframe(roles_2024[['DevType', 'Language', 'Growth']].head(20))

    # Conexión con el recomendador: Selección de rol
    selected_role = st.selectbox(
        "🔍 Selecciona un rol para explorar habilidades clave:",
        options=roles_2024['DevType'].unique()
    )

    if st.button(f"Buscar cursos relacionados con el rol **{selected_role}**"):
        # Intentar búsqueda con el rol completo
        recommendations = recommend_courses_function(
            courses_data=courses_data,
            model=model,
            keyword=selected_role,
            top_n=5
        )

        if isinstance(recommendations, str):  # Sin resultados con el rol completo
            st.warning(f"No se encontraron cursos relacionados con el rol completo: **{selected_role}**.")
            st.info("Resultados de búsqueda compuesta (palabra por palabra)")

            # Intentar búsquedas palabra por palabra
            keywords = selected_role.split()
            partial_recommendations = []
            found_keywords = []

            for word in keywords:
                partial_results = recommend_courses_function(
                    courses_data=courses_data,
                    model=model,
                    keyword=word,
                    top_n=3  # Reducimos el número de resultados parciales
                )
                if not isinstance(partial_results, str):  # Si hay resultados para la palabra
                    partial_recommendations.append(partial_results)
                    found_keywords.append(word)

            if partial_recommendations:
                # Combinar los resultados parciales
                combined_recommendations = pd.concat(partial_recommendations).drop_duplicates().reset_index(drop=True)
                st.markdown(f"### 📚 Cursos relacionados con palabras de **{selected_role}**:")
                st.write(f"Palabras clave utilizadas: {', '.join(found_keywords)}")
                st.dataframe(combined_recommendations)
            else:
                st.error("No se encontraron cursos relacionados ni con palabras parciales del rol.")
        else:
            st.markdown(f"### 📚 Cursos relacionados con el rol **{selected_role}**:")
            st.dataframe(recommendations.reset_index(drop=True))

    st.markdown("---")

    # Métodos de Aprendizaje
    st.subheader("📘 Métodos de Aprendizaje Preferidos")
    st.write(
        "Descubre cómo la comunidad prefiere aprender nuevas tecnologías. "
        "Esto incluye recursos en línea, libros, tutoriales, entre otros."
    )
    st.table(format_dataframe_with_ranking(learning_methods_2024, ['Method', 'TotalFrequency']))


def format_dataframe_with_ranking(df, columns, top_n=10):
    """
    Reindexa un DataFrame con índices del 1 al N para mostrar como un top.

    :param df: DataFrame a reindexar.
    :param columns: Columnas relevantes a mostrar.
    :param top_n: Número máximo de filas a mostrar.
    :return: DataFrame reindexado.
    """
    formatted_df = df[columns].head(top_n).reset_index(drop=True)
    formatted_df.index += 1  # Cambiar índice para que empiece desde 1
    return formatted_df


