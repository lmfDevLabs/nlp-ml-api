# packages
from flask import jsonify
# utilities
from app.utilities.text_processing_utils import preprocess_text_and_create_tags
from app.utilities.openai_embeddings_utils import generate_openai_embeddings
from app.utilities.openai_llm_utils import generate_response_via_chain
from app.utilities.cloud_storage_utils import download_docs_embeddings_from_gcs
from app.utilities.firestore_utils import create_tags_on_session_doc, save_response_to_firestore
from app.utilities.commom_embeddings_utils import search_docs_products, calculate_similarity
 

# to init the creation of embeddings from url pdf docs of products publish on fs db
def deal_with_incoming_chat_messages(product_snapshot):
    print("deal_with_incoming_chat_messages")
    try:
        # some data from product 
        new_message = product_snapshot
        seller_id = new_message['seller_id']
        user_id = new_message['user_id']
        user_question = new_message['user_question']
        session_id = new_message['session_id']
        showroom_id = new_message['showroom_id']

        # 1. Preprocesar la pregunta (extraer palabras clave)
        tags = preprocess_text_and_create_tags(user_question)

        # 2. salvar tags en sesion de usuario en db
        tags_on_db = create_tags_on_session_doc(tags)

        # 3. descargar el consolidado de embeddings de los pdf de los productos
        consolidated_file_path = f"{showroom_id}/products_pdf_embeddings_consolidate.json"
        products_pdf_embeddings_consolidate = download_docs_embeddings_from_gcs(consolidated_file_path)

        # 4. Calcular el embedding de la pregunta
        user_question_embedding = generate_openai_embeddings(user_question)

        # 5. Medicion para obtener solo los docs .json relevantes de entre todos los disponibles
        relevant_json_docs = calculate_similarity(user_question_embedding, products_pdf_embeddings_consolidate)
        
        # 6. Comparar con la base de datos de PDFs (vector store) para top 5
        matched_results = search_docs_products(user_question_embedding, products_pdf_embeddings_consolidate)
        
        # 7. Generar respuesta utilizando LLM
        response = generate_response_via_chain(user_question, relevant_json_docs)
        
        # 8. Guardar la respuesta en la base de datos de Firestore, en la sesión correcta
        status = save_response_to_firestore(user_id, session_id, response)
        
        # 9. Retornar respuesta
        return jsonify({
            'success': True, 
            'message': 'Embeddings generados y subidos con éxito',
            "question": user_question,
            "response": response,
            "matched_results": matched_results
        }), 200
    
    except Exception as e:
        print(f"Error en el procesamiento: {e}")
        return {'success': False, 'message': f"Error en el procesamiento: {e}"}