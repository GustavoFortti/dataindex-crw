import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json

def connection():
    cred = credentials.Certificate("./.env/nutrifind-22427-firebase-adminsdk-a45tv-ebfe521e9c.json")  # Substitua pelo caminho para o seu arquivo de credenciais Firebase
    firebase_admin.initialize_app(cred)
    db = firestore.client()

    return db

def insert(db, df, file_path):
    try:
        data_dict = df.to_dict(orient='records')
        for item in data_dict:
            _, doc_ref = db.collection('produtos').add(item)
            print(f'Documento adicionado com ID: {doc_ref.id}')

    except Exception as e:
        print(f"Erro ao enviar dados para o Firestore: {str(e)}")

def update(df, file_path):
    pass

def delete(db, ids):
    for id in ids:
        doc_ref = db.collection('produtos').document(id)
        doc_ref.delete()
        print(f"Documento {id} excluído com sucesso!")