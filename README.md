
# CourseMatch

**CourseMatch** es una herramienta de recomendación de cursos en línea desarrollada en [Streamlit](https://streamlit.io/). Utiliza inteligencia artificial y modelos avanzados de procesamiento de lenguaje natural (NLP) para ayudarte a encontrar cursos relevantes de plataformas como Coursera, Udacity, edX y más.

## 🚀 Características

- 🔍 **Búsqueda personalizada**: Encuentra cursos basados en palabras clave como "Python", "Machine Learning" o "JavaScript".
- ⚙️ **Filtros avanzados**: Ajusta el nivel del curso, calificaciones, popularidad, y más.
- 📚 **Recomendaciones relevantes**: Clasificación de cursos según tu interés y datos de popularidad.
- 🎯 **Interfaz amigable**: Panel lateral para configurar filtros y resultados claros en pantalla.

## 🛠️ Instalación y Configuración

1. Clona este repositorio:
   ```bash
   git clone https://github.com/tuusuario/CourseMatch.git
   cd CourseMatch
   ```

2. Crea un entorno virtual (opcional pero recomendado):
   ```bash
   python3 -m venv env
   source env/bin/activate  # En Windows: .\\env\\Scripts\\activate
   ```

3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Asegúrate de tener el dataset procesado. Si no está disponible, ejecuta el preprocesador:
   ```bash
   python app/preprocessor.py
   ```

5. Ejecuta la aplicación Streamlit:
   ```bash
   streamlit run app/app.py
   ```

## 📂 Estructura del Proyecto

```
CourseMatch/
│
├── notebooks/                  # Notebooks para desarrollo y experimentación
│   ├── model_development.ipynb
│
├── app/                        # Aplicación Streamlit
│   ├── app.py                  # Archivo principal de Streamlit
│   ├── preprocessor.py         # Limpieza y generación de embeddings
│   ├── recommender.py          # Función principal del modelo
│   └── __init__.py
│
├── data/                       # Datos y datasets
│   ├── courses_cleaned_dataset.csv
│   └── processed/
│       ├── courses_data.pkl
│
├── requirements.txt            # Dependencias del proyecto
├── README.md                   # Documentación del proyecto
└── LICENSE                     # Licencia del proyecto
```

## 🛡️ Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Si tienes ideas, mejoras o correcciones, no dudes en abrir un issue o enviar un pull request.

## 📬 Contacto

Para cualquier pregunta o sugerencia, puedes contactar a:
- Luca Ramirez(https://github.com/lucaramirezo)