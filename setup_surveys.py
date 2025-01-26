import os
import zipfile
import shutil


def extract_surveys():
    # Ruta del archivo .zip
    zip_path = os.path.join("app", "data", "surveys.zip")
    # Carpeta de destino
    dest_dir = os.path.join("app", "data", "surveys")

    # Verifica si el archivo .zip existe
    if not os.path.exists(zip_path):
        print(f"El archivo {zip_path} no existe. Asegúrate de que está en el lugar correcto.")
        return

    # Elimina la carpeta surveys si ya existe para evitar conflictos
    if os.path.exists(dest_dir):
        print(f"Eliminando la carpeta existente: {dest_dir}")
        shutil.rmtree(dest_dir)

    # Crea la carpeta surveys si no existe
    os.makedirs(dest_dir, exist_ok=True)

    # Extrae el contenido del .zip
    print(f"Extrayendo {zip_path} en {dest_dir}...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        for member in zip_ref.namelist():
            # Obtén el nombre base del archivo
            base_name = os.path.basename(member)
            # Solo extrae si no es una carpeta
            if base_name:
                # Extrae el archivo a la carpeta destino
                source = zip_ref.open(member)
                target = open(os.path.join(dest_dir, base_name), "wb")
                with source, target:
                    shutil.copyfileobj(source, target)

    print(f"Extracción completa. Archivos disponibles en {dest_dir}.")


if __name__ == "__main__":
    extract_surveys()
