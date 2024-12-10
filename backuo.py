# Importación de módulos necesarios para el proyecto
from rest_framework.response import Response  # Respuesta HTTP de Django REST framework
from rest_framework import status  # Códigos de estado HTTP
from rest_framework.views import APIView  # Vista base para la creación de APIs
import json  # Módulo para manejar JSON
from django.conf import settings  # Configuración del proyecto Django
import numpy as np  # Módulo para trabajar con matrices y cálculos numéricos
import faiss  # Módulo para índices de búsqueda eficientes en embeddings
from transformers import AutoTokenizer, AutoModel  # Herramientas para usar modelos de transformers de Hugging Face
import torch  # Módulo para usar PyTorch, la librería de machine learning
import os  # Módulo para manejar funciones del sistema operativo
from api_users.models import Usuario  # Importación del modelo 'Usuario' desde la app 'api_users'
from api_users.serializers import EmptySerializer  # Serializador vacío
from rest_framework.generics import GenericAPIView  # Vista genérica de Django REST Framework
import google.generativeai as genai  # Librería para usar Google Generative AI
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"  # Configuración para evitar errores de duplicación de librerías en PyTorch

# Cargar el archivo JSON que contiene los datos de las comidas y los embeddings generados
file_path = 'C:/Users/USUARIO/Documents/Inkapathways/Backend/inkapathways_backend/modelo_v1/comidas_con_embeddings.json'  # Ruta del archivo JSON con los datos
with open(file_path, 'r', encoding='utf-8') as f:
    comidas_cargadas = json.load(f)  # Cargar los datos desde el archivo JSON

# Cargar el modelo y el tokenizador del transformer de Hugging Face
model_name = 'sentence-transformers/all-distilroberta-v1'  # Modelo preentrenado de DistilRoBERTa para embeddings
tokenizer = AutoTokenizer.from_pretrained(model_name)  # Cargar el tokenizador
model = AutoModel.from_pretrained(model_name)  # Cargar el modelo preentrenado

# Preparar los embeddings de los documentos de las comidas, extraídos de los datos cargados
embeddings_documentos = [emb[0] for comida in comidas_cargadas for emb in comida['embeddings']]  # Obtener todos los embeddings
embeddings_documentos = np.array(embeddings_documentos, dtype=np.float32)  # Convertir los embeddings a un array de NumPy

# Crear un índice FAISS (una estructura eficiente para buscar en grandes cantidades de vectores)
index = faiss.IndexFlatL2(embeddings_documentos.shape[1])  # Usar FAISS con distancia L2 (euclidiana)
index.add(embeddings_documentos)  # Añadir los embeddings al índice

# Función para obtener el embedding de un texto dado
def obtener_embeddings(texto):
    inputs = tokenizer(texto, return_tensors='pt', truncation=True, padding=True)  # Tokenizar el texto
    with torch.no_grad():  # Desactivar el cálculo de gradientes, ya que no se entrena el modelo
        embeddings = model(**inputs).last_hidden_state.mean(dim=1)  # Obtener el embedding promedio del texto
    return embeddings  # Retornar el embedding calculado

# Vista para manejar la bienvenida de un usuario autenticado
class WelcomeView(GenericAPIView):
    serializer_class = EmptySerializer  # Usar un serializador vacío

    # Método POST para procesar la autenticación y mostrar un mensaje de bienvenida
    def post(self, request, *args, **kwargs):
        # Obtener el token de autenticación desde el encabezado de la solicitud
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:  # Si no se proporciona el token
            return Response({'error': 'Token no proporcionado'}, status=status.HTTP_400_BAD_REQUEST)

        # Verificar y extraer el token en formato Bearer
        parts = auth_header.split()
        if len(parts) == 2 and parts[0].lower() == 'bearer':
            token_verificacion = parts[1]
        elif len(parts) == 1:
            token_verificacion = parts[0]
        else:
            return Response({'error': 'Formato de token inválido'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Intentar encontrar al usuario en la base de datos con el token
            usuario = Usuario.objects.get(token_verificacion=token_verificacion)
        except Usuario.DoesNotExist:
            # Si el usuario no existe, devolver un error
            return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        # Si el usuario se encuentra, devolver un mensaje de bienvenida
        return Response({
            "message": f"Hola {usuario.nombre}, bienvenido a Inkapathways!",  # Mensaje de bienvenida personalizado
            "credenciales": {  # Información adicional del usuario
                "correo": usuario.correo,
                "nombre": usuario.nombre,
                "apellido": usuario.apellido,
                "region": usuario.region
            }
        }, status=status.HTTP_200_OK)

# Vista para manejar las consultas de comidas (búsqueda)
class SearchComidasAPIView(APIView):
    def post(self, request):
        consulta = request.data.get('consulta', '')  # Obtener la consulta desde los datos de la solicitud
        if not consulta:  # Si no se proporcionó una consulta
            return Response({"error": "No se proporcionó ninguna consulta"}, status=status.HTTP_400_BAD_REQUEST)

        # Obtener el embedding de la consulta usando el modelo
        embedding_consulta = obtener_embeddings(consulta).numpy().reshape(1, -1)
        
        # Buscar la consulta en el índice FAISS
        distancias, indices = index.search(embedding_consulta, k=5)  # Obtener los 5 resultados más cercanos

        resultados = []
        for i, idx in enumerate(indices[0]):
            # Calcular el índice de la comida y del dato a partir del índice obtenido
            comida_index = idx // len(comidas_cargadas[0]['embeddings'])
            dato_index = idx % len(comidas_cargadas[comida_index]['embeddings'])

            comida = comidas_cargadas[comida_index]  # Obtener la comida correspondiente
            dato = comida['datos'][dato_index]  # Obtener el dato correspondiente a la comida
            resultados.append({
                "comida": comida['comida'],  # Nombre de la comida
                "dato": dato,  # Dato relevante de la comida
                "distancia": float(distancias[0][i])  # Distancia del embedding, como medida de similitud
            })

        # Devolver la respuesta con los resultados encontrados
        return Response({"consulta": consulta, "resultados": resultados}, status=status.HTTP_200_OK)

# Vista para generar respuestas basadas en preguntas
class PreguntasAPI(APIView):
    def post(self, request):
        # Obtener el 'prompt' de la solicitud
        prompt = request.data.get("prompt")
        if not prompt:  # Si no se proporciona un prompt
            return Response({"error": "El campo 'prompt' es requerido."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Paso 1: Obtener contexto relevante usando la lógica de la vista 'SearchComidasAPIView'
        embedding_consulta = obtener_embeddings(prompt).numpy().reshape(1, -1)  # Obtener el embedding de la consulta
        distancias, indices = index.search(embedding_consulta, k=10)  # Buscar en el índice FAISS

        retrieved_context = []  # Lista para almacenar los fragmentos de contexto recuperados
        for i, idx in enumerate(indices[0]):
            comida_index = idx // len(comidas_cargadas[0]['embeddings'])
            dato_index = idx % len(comidas_cargadas[comida_index]['embeddings'])
            comida = comidas_cargadas[comida_index]
            dato = comida['datos'][dato_index]
            retrieved_context.append(f"{comida['comida']}: {dato}")

        # Unir los fragmentos de contexto recuperados en una cadena
        context_text = " ".join(retrieved_context[:3])  
        genai.configure(api_key=settings.GOOGLE_API_KEY)
        system_instruction = (
        "Tú eres un guía turístico y quieres generar interés en la comida peruana. "
        "Genera una nueva pregunta en cada ocasión con 4 alternativas para seleccionar, "
        "con el fin de conocer los gustos del turista de manera secuencial. "
        "Usa el idioma español y utiliza los siguientes fragmentos de contexto recuperado para  formular la pregunta. "
        "Crea cada pregunta a partir de la respuesta anterior proporcionada en {prompt}. "
        "Si no sabes la respuesta, indica que no sabes. "
        "Usa un máximo de tres oraciones y mantén la respuesta breve y concisa. "
        f"{context_text}"
)
        model = genai.GenerativeModel("models/gemini-1.5-flash")
        chat = model.start_chat()
        message_response = chat.send_message(f"{system_instruction}\n\n{prompt}").text
        # Paso 3: Usar el modelo generativo de Google AI para obtener la respuesta
        #genai.configure(api_key=settings.GOOGLE_API_KEY)  # Configurar la API de Google
        #model = genai.GenerativeModel("gemini-1.5-flash-latest", generation_config={"response_mime_type": "application/json"})  # Configurar el modelo generativo

        # Enviar el prompt al modelo generativo de Google
        #chat = model.start_chat()  # Iniciar una nueva conversación
        #message_response = chat.send_message(f"{system_instruction}\n\n{prompt}").text  # Obtener la respuesta del modelo generativo
        
        # Paso 4: Si no se encontró contexto relevante, usar el modelo para generar una respuesta
        if not retrieved_context:
            prompt = (  # Si no se encuentra contexto, ajustar el prompt
                "No se encontró contexto relevante. Responde directamente a la pregunta: " + prompt
            )
            response = model.start_chat(history=[{"text": prompt}]).text  # Obtener la respuesta
        else:
            response = message_response  
        # Retornar la respuesta generada
        return Response({"response": response}, status=status.HTTP_200_OK)