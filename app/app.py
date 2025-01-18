import streamlit as st
import pandas as pd
import joblib
from sentence_transformers import SentenceTransformer
from Model.recommender import recommend_courses_with_embeddings

# Cargar recursos
@st.cache_resource
def load_resources():
    courses_data = joblib.load('app/Model/data/processed/courses_data.pkl')  # Dataset preprocesado
    model = SentenceTransformer('all-MiniLM-L6-v2')  # Modelo de embeddings
    return courses_data, model

courses_data, model = load_resources()

# Mensaje de bienvenida
st.markdown(
    """
    <div style="background-color: #f4f4f4; padding: 15px; border-radius: 10px;">
        <h1 style="text-align: center; color: #4CAF50;">Bienvenido al Recomendador de Cursos</h1>
        <p style="text-align: center;">
            Esta aplicación utiliza inteligencia artificial para recomendarte cursos en línea 
            basados en tus intereses, nivel de experiencia, y calificaciones de los usuarios.
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
st.markdown("### 🗂 Resumen del Dataset")
total_courses = len(courses_data)
platform_counts = courses_data['Platform'].value_counts()
avg_rating = courses_data['Rating'].mean()
rating_range = (courses_data['Rating'].min(), courses_data['Rating'].max())
levels_available = courses_data['Level'].unique()

st.markdown(
    f"""
    - **Total de cursos disponibles:** {total_courses}
    - **Plataformas representadas:**
    """
)
for platform, count in platform_counts.items():
    st.markdown(f"  - {platform}: {count} cursos")
st.markdown(
    f"""
    - **Calificación promedio:** {avg_rating:.2f} (Rango: {rating_range[0]} - {rating_range[1]})
    - **Niveles disponibles:** {', '.join([f'Nivel {lvl}' for lvl in levels_available])}
    """
)

# Panel lateral para filtros
st.sidebar.header("🎯 Personaliza tu búsqueda")
keyword = st.sidebar.text_input("**Palabra clave (ej.: Python, Machine Learning, JavaScript):**", value="")
level = st.sidebar.selectbox("**Nivel del curso:**", options=["Todos"] + list(levels_available), format_func=lambda x: "Todos" if x == "Todos" else f"Nivel {x}")
rating_range = st.sidebar.slider("**Rango de calificación:**", min_value=0.0, max_value=5.0, value=(4.0, 5.0), step=0.1)
platform = st.sidebar.selectbox("**Plataforma:**", options=["Todas"] + list(courses_data['Platform'].unique()))
top_n = st.sidebar.number_input("**Número de recomendaciones:**", min_value=1, max_value=20, value=5)
popularity_weight = st.sidebar.slider("**Peso de la popularidad en las recomendaciones:**", min_value=0.0, max_value=1.0, value=0.5)

# Convertir entradas a valores válidos
level = None if level == "Todos" else int(level)
platform = None if platform == "Todas" else platform

# Botón de envío
if st.sidebar.button("🔍 Obtener recomendaciones"):
    if not keyword.strip():
        st.error("Por favor, ingresa una palabra clave.")
    else:
        recommendations = recommend_courses_with_embeddings(
            courses_data=courses_data,
            model=model,
            keyword=keyword,
            level=level,
            rating_range=rating_range,
            platform=platform,
            top_n=top_n,
            popularity_weight=popularity_weight
        )
        if isinstance(recommendations, str):  # No hay resultados
            st.warning(recommendations)
        else:
            st.markdown("### 📚 Cursos recomendados:")
            st.dataframe(recommendations)
