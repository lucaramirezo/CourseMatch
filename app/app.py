import streamlit as st
from components.tabs import render_courses_tab, render_trends_tab
from components.tendencies import (
    load_and_consolidate_surveys,
    calculate_language_trends,
    analyze_roles,
    analyze_learning_methods
)
from Model.recommender import recommend_courses_with_embeddings
import joblib
from sentence_transformers import SentenceTransformer

# Cargar recursos
@st.cache_resource
def load_resources():
    courses_data = joblib.load('app/data/processed/courses_data.pkl')  # Dataset preprocesado
    model = SentenceTransformer('all-MiniLM-L6-v2')  # Modelo de embeddings
    return courses_data, model

@st.cache_data
def load_trends():
    surveys_data = load_and_consolidate_surveys()
    trends_2024 = calculate_language_trends(surveys_data, 2024)
    roles_2024 = analyze_roles(surveys_data, 2024)
    learning_methods_2024 = analyze_learning_methods(surveys_data, 2024)
    return trends_2024, roles_2024, learning_methods_2024

# Cargar datos
courses_data, model = load_resources()
trends_2024, roles_2024, learning_methods_2024 = load_trends()

# Barra de navegación superior
selected_tab = st.selectbox(
    "Elige una sección:",
    ["Recomendador de Cursos", "Tendencias Tecnológicas"],
    key="main_navigation"
)

# Renderizar tabs según la selección
if selected_tab == "Recomendador de Cursos":
    render_courses_tab(courses_data, model, recommend_courses_with_embeddings)
elif selected_tab == "Tendencias Tecnológicas":
    render_trends_tab(trends_2024, roles_2024, learning_methods_2024)
