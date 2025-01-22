import streamlit as st
import pandas as pd
from .visualizations import (
    plot_language_trends,
    plot_learning_methods,
    plot_language_popularity_vs_growth, plot_role_language_scatter, plot_role_language_bubble,
    plot_role_language_stacked_bar, plot_learning_methods_comparison
)


# Tab: Recomendador de Cursos
def render_courses_tab(courses_data, model, recommend_courses_function):
    # Mensaje de bienvenida
    st.markdown(
        """
        <div style="background-color: #f4f4f4; padding: 15px; border-radius: 10px;">
            <h1 style="text-align: center; color: #4CAF50;">Bienvenido al Recomendador de Cursos</h1>
            <p style="text-align: center;">
                Esta aplicación utiliza inteligencia artificial para recomendarte cursos en línea 
                basados en tus intereses, nivel de experiencia y calificaciones de los usuarios.
            </p>
            <ul>
                <li>🔍 <b>Busca cursos</b> ingresando una palabra clave como <i>Python</i> o <i>JavaScript</i>.</li>
                <li>⚙️ <b>Personaliza</b> tus resultados ajustando filtros como nivel, plataforma y popularidad.</li>
                <li>📊 <b>Obtén recomendaciones</b> ordenadas por relevancia, popularidad y calificación.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Resumen descriptivo del dataset
    st.markdown("---")
    st.markdown("### 🗂 Resumen de los Datos")
    total_courses = len(courses_data)
    platform_counts = courses_data['Platform'].value_counts()
    avg_rating = courses_data['Rating'].mean()
    rating_range = (courses_data['Rating'].min(), courses_data['Rating'].max())
    levels_available = ", ".join(map(str, courses_data['Level'].unique()))

    st.markdown(
        f"""
        - **Total de cursos disponibles:** {total_courses}
        - **Plataformas representadas:**
        """
    )
    st.markdown(
        "".join([f"  - {platform}: {count} cursos\n" for platform, count in platform_counts.items()])
    )
    st.markdown(
        f"""
        - **Calificación promedio:** {avg_rating:.2f} (Rango: {rating_range[0]} - {rating_range[1]})
        - **Niveles disponibles:** {levels_available}
        """
    )

    # Panel lateral para filtros
    st.sidebar.header("🎯 Personaliza tu búsqueda")
    keyword = st.sidebar.text_input("**Palabra clave (ej.: Python, Machine Learning, JavaScript):**", value="")
    level = st.sidebar.selectbox("**Nivel del curso:**", options=["Todos"] + sorted(courses_data['Level'].unique()))
    rating_range = st.sidebar.slider("**Rango de calificación:**", min_value=0.0, max_value=5.0, value=(4.0, 5.0), step=0.1)
    platform = st.sidebar.selectbox("**Plataforma:**", options=["Todas"] + sorted(courses_data['Platform'].unique()))
    top_n = st.sidebar.number_input("**Número de recomendaciones:**", min_value=1, max_value=20, value=5)
    popularity_weight = st.sidebar.slider("**Peso de la popularidad:**", min_value=0.0, max_value=1.0, value=0.5)

    # Ajustar valores de filtros
    level = None if level == "Todos" else int(level)
    platform = None if platform == "Todas" else platform

    # Generar recomendaciones
    if st.sidebar.button("🔍 Obtener recomendaciones"):
        if not keyword.strip():
            st.error("Por favor, ingresa una palabra clave.")
        else:
            recommendations = recommend_courses_function(
                courses_data=courses_data,
                model=model,
                keyword=keyword.strip(),
                level=level,
                rating_range=rating_range,
                platform=platform,
                top_n=top_n,
                popularity_weight=popularity_weight
            )
            if isinstance(recommendations, str):
                st.warning(recommendations)
            elif recommendations.empty:
                st.warning("No se encontraron resultados para los filtros seleccionados.")
            else:
                st.markdown("### 📚 Cursos recomendados:")
                st.dataframe(recommendations)


def render_trends_tab(trends_2024, roles_2024, learning_methods_2024, courses_data, model, recommend_courses_function):
    # Introducción
    st.title("📊 Tendencias Tecnológicas")
    st.markdown(
        """
        Bienvenido a la sección de **Tendencias Tecnológicas**, basada en los datos de las encuestas anuales de 
        [Stack Overflow](https://survey.stackoverflow.co/). Aquí encontrarás:
        - Los lenguajes de programación y tecnologías más deseadas y en declive.
        - Roles emergentes y las habilidades clave asociadas.
        - Métodos de aprendizaje preferidos por la comunidad.

        **Enlaces a encuestas recientes**:
        - [Encuesta 2024](https://survey.stackoverflow.co/2024)
        - [Encuesta 2023](https://survey.stackoverflow.co/2023)
        - [Encuesta 2022](https://survey.stackoverflow.co/2022)
        """
    )
    st.markdown("---")

    # Selector entre gráficos y rankings
    view_option = st.radio(
        "Selecciona el modo de visualización:",
        options=["Gráficos", "Ranking"]
    )

    # Lenguajes en Auge y Declive
    with st.expander("📈 Lenguajes en Auge y Declive"):
        if view_option == "Gráficos":
            st.altair_chart(plot_language_trends(trends_2024), use_container_width=True)
        else:
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("### Lenguajes en Auge")
                top_languages = format_dataframe_with_ranking(trends_2024, ['Language', 'Growth'], top_n=5,
                                                              ascending=False)
                st.table(top_languages)

                # Botones para buscar cursos por lenguaje en auge
                st.markdown("#### Cursos Recomendados:")
                for _, row in top_languages.iterrows():
                    if st.button(f"Buscar cursos de {row['Language']}"):
                        recommendations = recommend_courses_function(
                            courses_data=courses_data,
                            model=model,
                            keyword=row['Language'],
                            top_n=5
                        )
                        if isinstance(recommendations, str):
                            st.warning(f"No se encontraron cursos relacionados con **{row['Language']}**.")
                        else:
                            st.markdown(f"### 📚 Cursos relacionados con **{row['Language']}**:")
                            st.dataframe(recommendations.reset_index(drop=True))

            with col2:
                st.markdown("### Lenguajes en Declive")
                st.table(format_dataframe_with_ranking(trends_2024, ['Language', 'Growth'], top_n=5, ascending=True))

    # Relación entre Roles y Lenguajes Clave
    with st.expander("👩‍💻 Relación entre Roles y Lenguajes Clave"):
        grouped_roles = group_roles_by_language(roles_2024)
        grouped_roles = clean_roles_dataframe(grouped_roles)

        if view_option == "Gráficos":
            # Selección de tipo de gráfico
            chart_option = st.radio(
                "Selecciona el tipo de visualización:",
                options=["Barras Apiladas", "Matriz de Burbujas", "Gráfico de Dispersión"]
            )
            if chart_option == "Barras Apiladas":
                st.altair_chart(plot_role_language_stacked_bar(grouped_roles), use_container_width=True)
            elif chart_option == "Matriz de Burbujas":
                st.altair_chart(plot_role_language_bubble(grouped_roles), use_container_width=True)
            elif chart_option == "Gráfico de Dispersión":
                st.altair_chart(plot_role_language_scatter(grouped_roles), use_container_width=True)
        else:
            st.markdown("### Tabla de Roles y Lenguajes (Top 10)")
            top_roles = grouped_roles.head(10)
            st.dataframe(top_roles)

            # Botones para buscar cursos por rol
            for _, row in top_roles.iterrows():
                if st.button(f"Buscar cursos para el rol {row['DevType']}"):
                    recommendations = recommend_courses_function(
                        courses_data=courses_data,
                        model=model,
                        keyword=row['DevType'],
                        top_n=5
                    )
                    if isinstance(recommendations, str):
                        st.warning(f"No se encontraron cursos relacionados con el rol **{row['DevType']}**.")
                    else:
                        st.markdown(f"### 📚 Cursos relacionados con el rol **{row['DevType']}**:")
                        st.dataframe(recommendations.reset_index(drop=True))

    # Métodos de Aprendizaje Más Populares
    with st.expander("📘 Métodos de Aprendizaje Más Populares"):
        if view_option == "Gráficos":
            st.altair_chart(plot_learning_methods(learning_methods_2024), use_container_width=True)
        else:
            st.table(
                format_dataframe_with_ranking(learning_methods_2024, ['Method', 'TotalFrequency'], maintain_order=True,
                                              top_n=10))


def render_learning_tab(learning_methods_2024):
    """
    Renderiza la sección 'Cómo Aprende la Gente Hoy en Día'.

    :param learning_methods_2024: DataFrame con datos de métodos de aprendizaje.
    """
    st.title("📘 Cómo Aprende la Gente Hoy en Día")
    st.markdown(
        """
        Esta sección explora las preferencias de aprendizaje actuales de la comunidad tecnológica, 
        basándonos en las encuestas recientes de Stack Overflow.

        Descubre:
        - **Métodos de aprendizaje más populares** (en línea y presenciales).
        - Comparativas entre enfoques educativos tradicionales y modernos.
        """
    )

    st.markdown("---")

    # Visualización: Métodos Populares
    st.subheader("📊 Métodos de Aprendizaje Más Populares")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Métodos en Línea")
        online_methods = learning_methods_2024[["Method", "OnlineFrequency"]].sort_values(
            by="OnlineFrequency", ascending=False
        ).head(5)
        st.table(format_dataframe_with_ranking(online_methods, columns=['Method', 'OnlineFrequency'], maintain_order=True))

    with col2:
        st.markdown("### Métodos Presenciales")
        # Filtrar métodos que no sean claramente presenciales
        offline_methods = learning_methods_2024[
            ~learning_methods_2024["Method"].str.contains("online", case=False)
        ][["Method", "OfflineFrequency"]].sort_values(by="OfflineFrequency", ascending=False).head(5)
        st.table(offline_methods)

    # Comparación gráfica de métodos
    st.markdown("---")
    st.subheader("🔍 Comparativa de Métodos en Línea y Presenciales")
    st.altair_chart(plot_learning_methods_comparison(learning_methods_2024), use_container_width=True)

    # Insights adicionales
    st.markdown("---")
    st.subheader("📈 Insights Adicionales")
    st.markdown(
        """
        - **Tendencia general**: Los métodos en línea dominan, pero los métodos presenciales aún son importantes 
        para roles altamente especializados o colaborativos.
        - **Preferencias modernas**: Bootcamps y plataformas de cursos masivos abiertos (MOOCs) son opciones populares 
        entre desarrolladores jóvenes.
        """
    )


def format_dataframe_with_ranking(df, columns, top_n=10, ascending=True, maintain_order=False):
    """
    Reindexa un DataFrame con índices del 1 al N para mostrar como un top ordenado o mantiene el orden original.

    :param df: DataFrame a reindexar.
    :param columns: Columnas relevantes a mostrar.
    :param top_n: Número máximo de filas a mostrar.
    :param ascending: Orden de los datos (ascendente o descendente).
    :param maintain_order: Si es True, no reordena y mantiene el orden original del DataFrame.
    :return: DataFrame reindexado.
    """
    if maintain_order:
        formatted_df = df[columns].head(top_n).reset_index(drop=True)
    else:
        formatted_df = df[columns].sort_values(by=columns[1], ascending=ascending).head(top_n).reset_index(drop=True)
    formatted_df.index += 1  # Cambiar índice para que empiece desde 1
    return formatted_df


def clean_roles_dataframe(df):
    """
    Limpia y ajusta el DataFrame para que sea compatible con Altair.

    :param df: DataFrame original con las columnas 'DevType', 'Languages', 'AvgPositiveGrowth', 'AvgNegativeGrowth'.
    :return: DataFrame limpio.
    """
    # Asegurar que las columnas numéricas tengan tipo float
    df['AvgPositiveGrowth'] = pd.to_numeric(df['AvgPositiveGrowth'], errors='coerce')
    df['AvgNegativeGrowth'] = pd.to_numeric(df['AvgNegativeGrowth'], errors='coerce')

    # Eliminar filas con valores nulos en las columnas críticas
    df = df.dropna(subset=['AvgPositiveGrowth', 'AvgNegativeGrowth', 'Languages', 'DevType'])

    # Reiniciar índice
    df.reset_index(drop=True, inplace=True)
    return df


def group_roles_by_language(roles_df):
    """
    Agrupa lenguajes por rol y calcula métricas de crecimiento promedio separadas (positivas y negativas).

    :param roles_df: DataFrame con columnas 'DevType', 'Language', y 'Growth'.
    :return: DataFrame con roles únicos, lenguajes agrupados, y métricas de crecimiento.
    """
    grouped = (
        roles_df
        .groupby('DevType')
        .agg(
            Languages=('Language', lambda x: ', '.join(sorted(set(x)))),  # Combina lenguajes únicos y ordenados
            AvgPositiveGrowth=('Growth', lambda g: g[g > 0].mean() if not g[g > 0].empty else 0.0),  # Promedio positivo
            AvgNegativeGrowth=('Growth', lambda g: g[g < 0].mean() if not g[g < 0].empty else 0.0)   # Promedio negativo
        )
        .reset_index()
    )
    # Convertir a tipo float explícitamente
    grouped['AvgPositiveGrowth'] = grouped['AvgPositiveGrowth'].astype(float)
    grouped['AvgNegativeGrowth'] = grouped['AvgNegativeGrowth'].astype(float)
    return grouped
