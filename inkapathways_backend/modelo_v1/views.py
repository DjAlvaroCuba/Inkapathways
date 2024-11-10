from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
import json
import numpy as np
import faiss
from transformers import AutoTokenizer, AutoModel
import torch
import os
from api_users.models import Usuario
from api_users.serializers import EmptySerializer
from rest_framework.generics import GenericAPIView

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
# Cargar el archivo JSON con los datos de las comidas y los embeddings
file_path = 'C:/Users/USUARIO/Documents/Inkapathways/Backend/inkapathways_backend/modelo_v1/comidas_con_embeddings.json'  # Cambia esta ruta si es necesario
with open(file_path, 'r', encoding='utf-8') as f:
    comidas_cargadas = json.load(f)

# Cargar el modelo y el tokenizador
model_name = 'sentence-transformers/all-distilroberta-v1'
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

# Preparar los embeddings de los documentos
embeddings_documentos = [emb[0] for comida in comidas_cargadas for emb in comida['embeddings']]
embeddings_documentos = np.array(embeddings_documentos, dtype=np.float32)

# Crear el índice FAISS
index = faiss.IndexFlatL2(embeddings_documentos.shape[1])
index.add(embeddings_documentos)

# Función para obtener embeddings de un texto
def obtener_embeddings(texto):
    inputs = tokenizer(texto, return_tensors='pt', truncation=True, padding=True)
    with torch.no_grad():
        embeddings = model(**inputs).last_hidden_state.mean(dim=1)
    return embeddings

class WelcomeView(GenericAPIView):
    serializer_class = EmptySerializer

    def post(self, request, *args, **kwargs):
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return Response({'error': 'Token no proporcionado'}, status=status.HTTP_400_BAD_REQUEST)

        parts = auth_header.split()
        if len(parts) == 2 and parts[0].lower() == 'bearer':
            token_verificacion = parts[1]
        elif len(parts) == 1:
            token_verificacion = parts[0]
        else:
            return Response({'error': 'Formato de token inválido'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            usuario = Usuario.objects.get(token_verificacion=token_verificacion)
        except Usuario.DoesNotExist:
            return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        return Response({
            "message": f"Hola {usuario.nombre}, bienvenido a Inkapathways!",
            "credenciales": {
                "correo": usuario.correo,
                "nombre": usuario.nombre,
                "apellido": usuario.apellido,
                "region": usuario.region
            }
        }, status=status.HTTP_200_OK)


class SearchComidasAPIView(APIView):
    def post(self, request):
        consulta = request.data.get('consulta', '')
        if not consulta:
            return Response({"error": "No se proporcionó ninguna consulta"}, status=status.HTTP_400_BAD_REQUEST)

        # Obtener el embedding de la consulta
        embedding_consulta = obtener_embeddings(consulta).numpy().reshape(1, -1)
        
        # Buscar en el índice FAISS
        distancias, indices = index.search(embedding_consulta, k=5)

        resultados = []
        for i, idx in enumerate(indices[0]):
            comida_index = idx // len(comidas_cargadas[0]['embeddings'])
            dato_index = idx % len(comidas_cargadas[comida_index]['embeddings'])

            comida = comidas_cargadas[comida_index]
            dato = comida['datos'][dato_index]
            resultados.append({
                "comida": comida['comida'],
                "dato": dato,
                "distancia": float(distancias[0][i])
            })

        return Response({"consulta": consulta, "resultados": resultados}, status=status.HTTP_200_OK)
