import pandas as pd
import os

# Directorio de los datos
DATA_DIR = os.path.join(os.path.dirname(__file__), "../data/surveys")

# Función para cargar y consolidar datasets
def load_and_consolidate_surveys():
    """
    Carga los datasets de encuestas y consolida los datos relevantes.

    :return: DataFrame consolidado con columnas clave y años.
    """
    files = {
        "2022": os.path.join(DATA_DIR, "survey_results_public_2022.csv"),
        "2023": os.path.join(DATA_DIR, "survey_results_public_2023.csv"),
        "2024": os.path.join(DATA_DIR, "survey_results_public_2024.csv")
    }
    columns_of_interest = [
        "LanguageHaveWorkedWith",
        "LanguageWantToWorkWith",
        "DevType",
        "LearnCode",
        "LearnCodeOnline"
    ]
    combined_data = pd.DataFrame()

    for year, file_path in files.items():
        df = pd.read_csv(file_path)
        if all(col in df.columns for col in columns_of_interest):
            temp_df = df[columns_of_interest].copy()
            temp_df["Year"] = int(year)
            combined_data = pd.concat([combined_data, temp_df], ignore_index=True)

    return combined_data

# Función para calcular tendencias de lenguajes
def calculate_language_trends(data, year):
    """
    Calcula los lenguajes en auge y declive para un año específico.

    :param data: DataFrame consolidado.
    :param year: Año para el análisis.
    :return: DataFrame con tendencias de lenguajes.
    """
    def count_language_frequencies(data, column):
        filtered_data = data[data["Year"] == year][column].dropna()
        # Separar lenguajes en listas individuales
        languages = filtered_data.str.split(";").explode()
        # Contar frecuencias
        result = languages.value_counts().reset_index()
        result.columns = ["Language", "Frequency"]  # Renombrar columnas explícitamente
        return result

    usage = count_language_frequencies(data[data["Year"] == year], "LanguageHaveWorkedWith")
    desired = count_language_frequencies(data[data["Year"] == year], "LanguageWantToWorkWith")

    trends = pd.merge(usage, desired, on="Language", how="outer", suffixes=("_Used", "_Desired")).fillna(0)
    trends["Growth"] = trends["Frequency_Desired"] - trends["Frequency_Used"]
    return trends.sort_values(by="Growth", ascending=False)

# Función para analizar roles y habilidades clave
def analyze_roles(data, year):
    filtered_data = data[data["Year"] == year][["DevType", "LanguageHaveWorkedWith", "LanguageWantToWorkWith"]].dropna()
    filtered_data["DevType"] = filtered_data["DevType"].str.split(";").explode()

    role_language_worked = filtered_data.assign(Language=filtered_data["LanguageHaveWorkedWith"].str.split(";")).explode("Language")
    role_language_desired = filtered_data.assign(Language=filtered_data["LanguageWantToWorkWith"].str.split(";")).explode("Language")

    worked = role_language_worked.groupby(["DevType", "Language"]).size().reset_index(name="WorkedFrequency")
    desired = role_language_desired.groupby(["DevType", "Language"]).size().reset_index(name="DesiredFrequency")

    trends = pd.merge(worked, desired, on=["DevType", "Language"], how="outer").fillna(0)
    trends["Growth"] = trends["DesiredFrequency"] - trends["WorkedFrequency"]
    return trends.sort_values(by=["DevType", "Growth"], ascending=[True, False])

# Función para analizar métodos de aprendizaje
def analyze_learning_methods(data, year):
    filtered_data = data[data["Year"] == year]
    offline_methods = filtered_data["LearnCode"].dropna().str.split(";").explode()
    online_methods = filtered_data["LearnCodeOnline"].dropna().str.split(";").explode()

    offline_frequencies = offline_methods.value_counts().reset_index()
    offline_frequencies.columns = ["Method", "OfflineFrequency"]

    online_frequencies = online_methods.value_counts().reset_index()
    online_frequencies.columns = ["Method", "OnlineFrequency"]

    learning_methods = pd.merge(offline_frequencies, online_frequencies, on="Method", how="outer").fillna(0)
    learning_methods["TotalFrequency"] = learning_methods["OfflineFrequency"] + learning_methods["OnlineFrequency"]

    return learning_methods.sort_values(by="TotalFrequency", ascending=False)

# Exportar funciones para uso en la app
__all__ = ["load_and_consolidate_surveys", "calculate_language_trends", "analyze_roles", "analyze_learning_methods"]
