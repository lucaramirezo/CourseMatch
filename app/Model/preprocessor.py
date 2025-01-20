import os
import joblib
import pandas as pd
from sentence_transformers import SentenceTransformer

# Crear las carpetas necesarias
os.makedirs('../data/processed', exist_ok=True)

# Cargar y procesar
def load_and_preprocess_data(file_path):
    courses_data = pd.read_csv(file_path)
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # Limpieza y generación de embeddings
    def clean_text(text):
        return ' '.join(str(text).lower().replace(',', ' ').split())

    courses_data['Cleaned_Skills'] = courses_data['Skills'].apply(clean_text)
    courses_data['Embeddings'] = courses_data['Cleaned_Skills'].apply(
        lambda x: model.encode(x, show_progress_bar=False)
    )

    # Guardar el archivo
    joblib.dump(courses_data, '../data/processed/courses_data.pkl')
    return courses_data, model

# Ejecutar el preprocesamiento
load_and_preprocess_data('../data/courses_cleaned_dataset.csv')
