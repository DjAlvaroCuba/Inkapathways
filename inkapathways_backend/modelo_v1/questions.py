#import json
#from django.conf import settings
#import google.generativeai as genai
#from api_users.authentication import TokenAuthentication
#from rest_framework.permissions import IsAuthenticated
#
#
#def generate_question(previous_question, previous_response, faiss_results):
#    # Configuración de la API de Google Generative AI
#    genai.configure(api_key=settings.GOOGLE_API_KEY)
#    model = genai.GenerativeModel("gemini-1.5-flash-latest", generation_config=#{"response_mime_type": "application/json"})
#
#    # Construir el contexto desde los resultados FAISS
#    context_fragments = "\n".join([f"- {comida['comida']}: {dato}" for comida, dato in #faiss_results])
#
#    # Crear el prompt de sistema
#    system_prompt = (
#        "Tú eres un asistente para tareas de respuesta a preguntas. "
#        "Usa los siguientes fragmentos de contexto recuperado para responder "
#        "la pregunta. Si no sabes la respuesta, di que no sabes. "
#        "Usa un máximo de tres oraciones y mantén la respuesta concisa.\n\n"
#        f"{context_fragments}"
#    )
#
#    # Crear el prompt para la generación de preguntas
#    prompt = f"""
#    Genera 5 preguntas de preferencia relacionadas a: {previous_question}.
#    Contexto adicional:
#    {system_prompt}
#    """
#
#    # Generar el contenido
#    raw_response = model.generate_content(prompt)
#    response = json.loads(raw_response.text)
#    print("total_tokens: ", model.count_tokens(prompt))
#    return response
#