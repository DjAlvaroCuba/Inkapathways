#import json
#from transformers import AutoTokenizer, AutoModel
#import torch
#import numpy as np
#import faiss
#import os
#os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
#
## 1. Cargar el archivo JSON
#file_path = 'C:/Users/USUARIO/Documents/Inkapathways/Backend/inkapathways_backend/modelo_v1/#pdf_juninv1.2.json'
#with open(file_path, 'r', encoding='utf-8') as f:
#    comidas = json.load(f)
#
## 2. Cargar el tokenizador y el modelo preentrenado
#model_name = 'sentence-transformers/all-distilroberta-v1'
#tokenizer = AutoTokenizer.from_pretrained(model_name)
#model = AutoModel.from_pretrained(model_name)
#
## 3. Función para obtener embeddings de un fragmento de texto
#def obtener_embeddings(texto):
#    inputs = tokenizer(texto, return_tensors='pt', truncation=True, padding=True)
#    with torch.no_grad():
#        embeddings = model(**inputs).last_hidden_state.mean(dim=1)
#    return embeddings
#
## 4. Generar los embeddings para los fragmentos de datos de cada comida
#for comida in comidas:
#    comida['embeddings'] = [obtener_embeddings(dato).numpy().tolist() for dato in comida#['datos']]
#
## 5. Guardar el archivo JSON con embeddings
#with open('comidas_con_embeddings.json', 'w') as f:
#    json.dump(comidas, f)
#
## 6. Cargar el archivo JSON con los embeddings
#with open('comidas_con_embeddings.json', 'r') as f:
#    comidas_cargadas = json.load(f)
#
## 7. Convertir los embeddings de los documentos a un array de numpy (flatten para los datos)
#embeddings_documentos = []
#for comida in comidas_cargadas:
#    for emb in comida['embeddings']:
#        embeddings_documentos.append(emb[0])  # Aplanamos el embedding, eliminando la capa extra #de lista
#
#embeddings_documentos = np.array(embeddings_documentos, dtype=np.float32)
#
## 8. Crear un índice FAISS
#index = faiss.IndexFlatL2(embeddings_documentos.shape[1])  # L2 es para calcular la distancia #euclidiana
#
## 9. Agregar los embeddings de los documentos al índice
#index.add(embeddings_documentos)
#
## 10. Consulta de ejemplo
#consulta = "Alvaro"
#embedding_consulta = obtener_embeddings(consulta).numpy().reshape(1, -1)
#
## 11. Buscar los 5 documentos más relevantes
#distancias, indices = index.search(embedding_consulta, k=2)
#
## 12. Mostrar los documentos más relevantes
#print(f"Consulta: {consulta}")
#print("Resultados más cercanos:")
#for i, idx in enumerate(indices[0]):
#    comida_index = idx // len(comidas_cargadas[0]['embeddings'])  # Determinar el índice de la #comida
#    dato_index = idx % len(comidas_cargadas[comida_index]['embeddings'])  # Determinar el índice #del dato
#
#    comida = comidas_cargadas[comida_index]
#    dato = comida['datos'][dato_index]
#    print(f"\nComida: {comida['comida']}")
#    print(f"  Dato: {dato}")
#    print(f"  Distancia: {distancias[0][i]}")
    
