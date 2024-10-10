# imports 
from app.utilities.pdf_utils import process_pdf_url, process_pdf_text
from app.utilities.commom_embeddings_utils import generate_chunk_embeddings
from app.utilities.cloud_storage_utils import upload_seller_embeddings_to_gcs
from app.utilities.cloud_storage_utils import update_on_gcs_consolidated_json

# to init the creation of embeddings from url pdf docs of products publish on fs db
def create_products_docs_embeddings(product_snapshot):
    print("create_products_docs_embeddings")
    try: 
        # some data from product 
        new_product = product_snapshot
        seller_id = new_product['sellerData']['sellerId']   
        company_name = new_product['sellerData']['companyName']
        pdf_url = new_product['pdf']
        car_model = new_product['car_model'] 
        showroom_id = new_product['showRoomData']['showRoomId']
        product_id = new_product['productId']

        # 1. Descargar y procesar el PDF 
        pdf_text, status = process_pdf_url(pdf_url)
        if not pdf_text:
            return {'success': False, 'message': 'No se pudo extraer el texto del PDF'}

        # 2. Creacion de chunks
        processed_chunks = process_pdf_text(pdf_text)
        if not processed_chunks:
            return {'success': False, 'message': 'No se pudieron generar los chunks'}
        
        # 3. Generar embeddings para cada chunk y almacenar los resultados
        chunks_data = generate_chunk_embeddings(car_model,processed_chunks)

        # 4. Guardar embeddings en Cloud Storage
        embeddings_data = {
            'companyName': company_name,
            'sellerId': seller_id,
            'productId': product_id,
            'vector': chunks_data
        }  
         
        # 5. register embeddings file for seller
        status = upload_seller_embeddings_to_gcs(seller_id, company_name, showroom_id, embeddings_data)

        # 6. Create the single source of truhth of products pdf embeddings
        consolidated_file_path = f"{showroom_id}/products_pdf_embeddings_consolidate.json"
        update_result = update_on_gcs_consolidated_json(embeddings_data, consolidated_file_path)

        if not update_result['success']:
            return update_result  # Si hubo un error actualizando el archivo, retornarlo.

        # 7. retornar respuesta
        return { 
            'success': True, 
            'message': 'Embeddings generados y subidos con éxito'
        }
    
    except Exception as e:
        print(f"Error en el procesamiento: {e}")
        return {'success': False, 'message': f"Error en el procesamiento: {e}"}