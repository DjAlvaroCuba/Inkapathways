# api/questions.py
import json
from django.conf import settings
import google.generativeai as genai
from api_users.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
def load_data_from_file(file_path):
    
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()
    
def generate_question(previous_question, previous_response):
    
    genai.configure(api_key=settings.GOOGLE_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash-latest", generation_config={"response_mime_type": "application/json"})

    file_path = 'modelo_v1/datos.txt'
    additional_info = load_data_from_file(file_path)

    prompt = f"""
    Basado en la respuesta anterior: "{previous_response}" a la pregunta: "{previous_question}", 
    y considerando la siguiente información: "{additional_info}",
    genera una nueva pregunta relacionada sobre preferencias gastronómicas 
    Responde en formato JSON: {{ 'pregunta': str, 'opciones': list[str] }}
    """

    raw_response = model.generate_content(prompt)
    response = json.loads(raw_response.text)
    print("total_tokens: ", model.count_tokens(prompt))
    return response
