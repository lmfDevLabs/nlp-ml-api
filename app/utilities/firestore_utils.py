from flask import request, jsonify
import numpy as np
import json
import os
from google.cloud import db, firestore


# BUYERS 
# para guardar tags en sessionId
def create_tags_on_session_doc(session_id, tags):

    """
    Guarda un array de tags en un documento de una sesión en Firestore.
    
    Args:
        session_id (str): El ID de la sesión donde se almacenarán los tags.
        tags (list): Una lista de tags a guardar en el documento de la sesión.
        
    Returns:
        bool: True si los tags se guardaron exitosamente, False en caso de error.
    """
    print("create_tags_on_session_doc")
    try:
        # Referencia al documento en la colección "sessions"
        doc_ref = db.collection('chats').document('session_id').collection('sessions').document(session_id)

        # Actualizar el documento con los tags
        doc_ref.set({
            'tags': tags
        }, merge=True)  # merge=True asegura que no se sobrescriban otros campos existentes

        print(f"Tags guardados exitosamente en la sesión {session_id}")
        return True
    except Exception as e:
        print(f"Error al guardar tags en la sesión {session_id}: {e}")
        return False

# para salvar respuesta en la sesion de chat
def save_response_to_firestore(user_id, session_id, response):
    print("save_response_to_firestore")
    try:
        # Referencia al documento en la colección "sessions"
        doc_ref = db.collection('chats').document('session_id').collection('sessions').document(session_id).collection('messages')

        # Actualizar el documento con los tags
        doc_ref.set({
            'content':response,
            'role':'assitant',
            'createdAt': firestore.SERVER_TIMESTAMP
        }, merge=True)  # merge=True asegura que no se sobrescriban otros campos existentes

        print(f"Tags guardados exitosamente en la sesión {session_id}")
        return True
    except Exception as e:
        print(f"Error al guardar tags en la sesión {session_id}: {e}")
        return False