from django.apps import AppConfig
import json
import numpy as np
import torch
from transformers import AutoTokenizer, AutoModel
import os

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
class ModeloV1Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'modelo_v1'

    def ready(self):
        # Ejecutar el proceso de generación de embeddings al iniciar el proyecto
        self.generar_embeddings()

    def generar_embeddings(self):
        # Cargar el archivo JSON con los datos de las comidas
        file_path = 'C:/Users/USUARIO/Documents/Inkapathways/Backend/inkapathways_backend/modelo_v1/pdf_juninv1.2.json'  # Cambia esta ruta si es necesario
        with open(file_path, 'r', encoding='utf-8') as f:
            comidas = json.load(f)

        # Cargar el modelo y el tokenizador
        model_name = 'sentence-transformers/all-distilroberta-v1'
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModel.from_pretrained(model_name)

        # Función para obtener embeddings de un texto
        def obtener_embeddings(texto):
            inputs = tokenizer(texto, return_tensors='pt', truncation=True, padding=True)
            with torch.no_grad():
                embeddings = model(**inputs).last_hidden_state.mean(dim=1)
            return embeddings

        # Generar los embeddings para las comidas
        for comida in comidas:
            comida['embeddings'] = [obtener_embeddings(dato).numpy().tolist() for dato in comida['datos']]

        # Obtener la ruta de la carpeta actual de la app (modelo_v1)
        app_directory = os.path.dirname(os.path.abspath(__file__))

        # Crear la ruta de salida para el archivo en la misma carpeta
        output_file_path = os.path.join(app_directory, 'comidas_con_embeddings.json')

        # Guardar el archivo JSON con los embeddings generados
        with open(output_file_path, 'w', encoding='utf-8') as f:
            json.dump(comidas, f, ensure_ascii=False, indent=4)

        print(f"Embeddings generados y archivo guardado como '{output_file_path}'.")
