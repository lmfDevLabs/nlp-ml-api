# packages
from flask import Blueprint, request, jsonify
# handlers
from app.handlers.docs_product_handler import create_products_docs_embeddings
from app.handlers.chat_messages_handler import deal_with_incoming_chat_messages

# bp 
main_bp = Blueprint('main', __name__)

## ROUTES
# hello world
@main_bp.route('/')
def index():
    return 'Hello, World!'

# Ruta para procesar productos
@main_bp.route('/process-product-docs', methods=['POST'])
def process_product_docs():
    print("process_product_docs")
    # raw data
    data = request.json  
    # some data
    product_id = data.get('productId')
    seller_data = data.get('sellerData')
    showroom_data = data.get('showRoomData')
    pdf_url = data.get('pdf')
    car_model= data.get('car_model')

    # Verificar si la URL del PDF está vacía o es None
    if not pdf_url:
        return jsonify({'success': False, 'message': 'La URL del PDF está vacía o no se proporcionó.'}), 400

    # Llamar a la función que maneja el procesamiento del producto
    try: 
        result = create_products_docs_embeddings({
            'sellerData': seller_data, 
            'showRoomData': showroom_data,
            'pdf': pdf_url,
            'productId': product_id,
            'car_model': car_model
        })

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    
# Ruta para procesar mensajes en las sesiones de chat
@main_bp.route('/process-chat-message', methods=['POST'])
def process_chat_message():
    print("process_chat_message")
    # Datos que provienen de la solicitud
    data = request.json  
    # extract some data
    user_question = data.get('content', "")
    user_id = data.get('userId', "")
    session_id = data.get('sessionId', "")
    showroom_id = data.get('show_room_id', "")
    
    if not user_question:
        return jsonify({"error": "No question provided"}), 400
    
    try:
        result = deal_with_incoming_chat_messages({
            "showroom_id":showroom_id,
            "user_id":user_id,
            "session_id":session_id,
            "user_question":user_question,
        })

        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500 