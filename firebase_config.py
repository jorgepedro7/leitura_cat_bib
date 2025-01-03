import firebase_admin
from firebase_admin import credentials, firestore
import pyrebase

# Inicializando o Firebase Admin SDK
if not firebase_admin._apps:
    cred = credentials.Certificate("secrets/leitura-catecismo-biblia-firebase-adminsdk-a7xzn-a1d913db16.json")
    firebase_admin.initialize_app(cred)

# Inicializando o Firestore para manipular o banco de dados
db = firestore.client()

# Configuração do Pyrebase para autenticação
firebase_config = {
    "apiKey": "AIzaSyDwVyQ8l2RfkUAl1Erbg6iHVqLij7C_nTE",
    "authDomain": "leitura-catecismo-biblia.firebaseapp.com",
    "projectId": "leitura-catecismo-biblia",
    "storageBucket": "leitura-catecismo-biblia.firebasestorage.app",
    "messagingSenderId": "223462113454",
    "appId": "1:223462113454:web:32c18d3c24cc02cd9ead3f",
    "databaseURL": "G-JKZPMYJ6JS"  # Deixe vazio se não for usar Realtime Database
}

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()
