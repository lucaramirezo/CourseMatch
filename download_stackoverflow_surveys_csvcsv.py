import os
import requests
import zipfile
from io import BytesIO

# URLs de los archivos ZIP
FILES = {
    "2022": "https://cdn.sanity.io/files/jo7n4k8s/production/stack-overflow-developer-survey-2022.zip",
    "2023": "https://cdn.sanity.io/files/jo7n4k8s/production/stack-overflow-developer-survey-2023.zip",
    "2024": "https://cdn.sanity.io/files/jo7n4k8s/production/262f04c41d99fea692e0125c342e446782233fe4.zip/stack-overflow-developer-survey-2024.zip",
}

# Directorio donde se guardarán los datos descomprimidos
OUTPUT_DIR = "app/data/surveys"

# Crear el directorio de salida si no existe
os.makedirs(OUTPUT_DIR, exist_ok=True)

def download_and_extract(url, output_dir):
    """Descarga y extrae un archivo ZIP desde una URL."""
    print(f"Downloading: {url}")
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with zipfile.ZipFile(BytesIO(response.content)) as zip_file:
            zip_file.extractall(output_dir)
        print(f"Extracted files to: {output_dir}")
    else:
        print(f"Failed to download: {url}. Status code: {response.status_code}")

# Descargar y extraer los datos
for year, url in FILES.items():
    print(f"Processing data for {year}...")
    download_and_extract(url, OUTPUT_DIR)
print("All surveys downloaded and extracted.")
