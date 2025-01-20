# CourseMatch

**CourseMatch** es una herramienta de recomendación de cursos en línea desarrollada en [Streamlit](https://streamlit.io/). Utiliza inteligencia artificial y modelos avanzados de procesamiento de lenguaje natural (NLP) para ayudarte a encontrar cursos relevantes de plataformas como Coursera, Udacity, edX y más.

Además, incluye una sección de **Tendencias Tecnológicas**, donde puedes explorar las habilidades, roles y métodos de aprendizaje más populares basados en datos de encuestas recientes de Stack Overflow.

## 🚀 Características

- 🔍 **Búsqueda personalizada**: Encuentra cursos basados en palabras clave como "Python", "Machine Learning" o "JavaScript".
- ⚙️ **Filtros avanzados**: Ajusta el nivel del curso, calificaciones, popularidad, y más.
- 📚 **Recomendaciones relevantes**: Clasificación de cursos según tu interés y datos de popularidad.
- 📊 **Tendencias Tecnológicas**: Explora los lenguajes en auge, roles emergentes, y métodos de aprendizaje más utilizados.
- 🎯 **Interfaz amigable**: Barra de navegación para alternar entre el recomendador de cursos y las tendencias.

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

## 📊 Survey Data

Los archivos de datos de las encuestas de Stack Overflow no están incluidos en este repositorio debido a restricciones de tamaño. Puedes descargarlos desde el sitio oficial de las encuestas:

- [Survey Results 2022](https://survey.stackoverflow.co/2022/)
- [Survey Results 2023](https://survey.stackoverflow.co/2023/)
- [Survey Results 2024](https://survey.stackoverflow.co/2024/)

Alternativamente, puedes usar el script `download_stackoverflow_surveys.py` incluido en este proyecto para automatizar la descarga y extracción de los datos:

### Descarga Automática de Datos

1. Instala la dependencia necesaria:
   ```bash
   pip install requests
   ```

2. Ejecuta el script para descargar y extraer los datos:
   ```bash
   python download_stackoverflow_surveys.py
   ```

3. Los datos se guardarán en el siguiente directorio:
   ```
   app/data/surveys/
   ├── survey_results_public_2022.csv
   ├── survey_results_public_2023.csv
   ├── survey_results_public_2024.csv
   ├── survey_results_schema_2022.csv
   ├── survey_results_schema_2023.csv
   └── survey_results_schema_2024.csv
   ```

---

## 📂 Estructura del Proyecto

```
CourseMatch/
│
├── notebooks/                  # Notebooks para desarrollo y experimentación
│   ├── model_development.ipynb
│   ├── TendencyEDA.ipynb
│
├── app/                        # Aplicación Streamlit
│   ├── app.py                  # Archivo principal de Streamlit
│   ├── components/             # Componentes modulares de la app
│   │   ├── tabs.py             # Definición de los tabs de la app
│   │   ├── tendencies.py       # Lógica de tendencias tecnológicas
│   │   └── ui_helpers.py       # Funciones auxiliares de interfaz
│   ├── data/                   # Datos y datasets
│   │   ├── courses_cleaned_dataset.csv
│   │   └── processed/
│   │       ├── courses_data.pkl
│   │       └── surveys/
│   │           ├── survey_results_public_2022.csv
│   │           ├── survey_results_public_2023.csv
│   │           └── survey_results_public_2024.csv
│   ├── Model/                  # Modelos y preprocesamiento
│   │   ├── recommender.py
│   │   ├── preprocessor.py
│   │   └── __init__.py
│   └── __init__.py
│
├── requirements.txt            # Dependencias del proyecto
├── download_stackoverflow_surveys.py  # Script para descargar encuestas
├── README.md                   # Documentación del proyecto
└── LICENSE                     # Licencia del proyecto
```

## 🛡️ Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Si tienes ideas, mejoras o correcciones, no dudes en abrir un issue o enviar un pull request.

## 📬 Contacto

Para cualquier pregunta o sugerencia, puedes contactar a:
- [Luca Ramirez](https://github.com/lucaramirezo)
