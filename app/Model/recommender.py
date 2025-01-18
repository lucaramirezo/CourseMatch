import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

def recommend_courses_with_embeddings(
    courses_data, model, keyword, level=None, rating_range=(0.0, 5.0), platform=None, top_n=5, popularity_weight=0.5
):
    """
    Recomienda cursos utilizando embeddings basados en habilidades, calificaciones y popularidad.

    :param courses_data: DataFrame preprocesado que incluye 'Cleaned_Skills', 'Embeddings', etc.
    :param model: Modelo de embeddings (SentenceTransformer).
    :param keyword: Palabra clave para buscar en las habilidades.
    :param level: Nivel del curso (0: Básico, 1: Intermedio, 2: Avanzado). Si es None, no filtra por nivel.
    :param rating_range: Rango de calificaciones (min, max).
    :param platform: Plataforma específica para filtrar los cursos. Si es None, no filtra por plataforma.
    :param top_n: Número de recomendaciones a devolver.
    :param popularity_weight: Peso de la popularidad en la ordenación (entre 0 y 1).
    :return: DataFrame con cursos recomendados ordenados por relevancia o un mensaje de error.
    """
    # Validar entradas del usuario
    if not keyword or not isinstance(keyword, str):
        raise ValueError("El parámetro 'keyword' debe ser una cadena no vacía.")
    if level is not None and level not in courses_data['Level'].unique():
        raise ValueError(f"El parámetro 'level' debe ser uno de {courses_data['Level'].unique().tolist()} o None.")
    if not isinstance(rating_range, tuple) or len(rating_range) != 2 or not (0.0 <= rating_range[0] <= 5.0) or not (0.0 <= rating_range[1] <= 5.0):
        raise ValueError("El parámetro 'rating_range' debe ser una tupla (min, max) con valores entre 0 y 5.")
    if platform and platform not in courses_data['Platform'].unique():
        raise ValueError(f"El parámetro 'platform' debe ser una de las plataformas disponibles: {courses_data['Platform'].unique().tolist()} o None.")
    if not isinstance(top_n, int) or top_n <= 0:
        raise ValueError("El parámetro 'top_n' debe ser un entero mayor a 0.")

    # Filtro por palabra clave
    filtered_courses = courses_data[
        courses_data['Cleaned_Skills'].str.contains(keyword.lower(), na=False)
    ]

    # Filtro por nivel (si se especifica)
    if level is not None:
        filtered_courses = filtered_courses[filtered_courses['Level'] == level]

    # Filtro por rango de calificaciones
    filtered_courses = filtered_courses[
        (filtered_courses['Rating'] >= rating_range[0]) & (filtered_courses['Rating'] <= rating_range[1])
    ]

    # Filtro por plataforma (si se especifica)
    if platform:
        filtered_courses = filtered_courses[filtered_courses['Platform'].str.contains(platform, na=False)]

    # Si no hay cursos después del filtro, retornar un mensaje
    if filtered_courses.empty:
        return "No se encontraron cursos que coincidan con los criterios especificados."

    # Obtener embedding del keyword ingresado
    keyword_embedding = model.encode(keyword.lower(), show_progress_bar=False)

    # Calcular similitud con los cursos filtrados
    filtered_embeddings = list(filtered_courses['Embeddings'])
    similarity_scores = cosine_similarity([keyword_embedding], filtered_embeddings)[0]

    # Crear DataFrame temporal con similitud
    filtered_courses = filtered_courses.copy()
    filtered_courses['Similarity'] = similarity_scores

    # Incorporar popularidad en la ordenación
    filtered_courses['Relevance'] = (
        (1 - popularity_weight) * filtered_courses['Similarity'] +
        popularity_weight * (filtered_courses['Number of students'] / filtered_courses['Number of students'].max())
    )

    # Ordenar por relevancia y eliminar duplicados
    recommendations = filtered_courses.sort_values(
        by=['Relevance', 'Rating'], ascending=[False, False]
    ).drop_duplicates(subset=['Course_Name', 'Platform']).head(top_n)

    return recommendations[['Course_Name', 'Platform', 'Rating', 'Level', 'Skills', 'Similarity', 'Relevance']]
