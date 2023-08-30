from firebase_admin import firestore_async, auth, credentials, initialize_app, storage
from service import service
from dotenv import load_dotenv

load_dotenv()
cred = credentials.Certificate(cert=service)
firebase_app = initialize_app(cred)
db = firestore_async.client(app=firebase_app)
auth = auth.Client(app=firebase_app)


storage = storage.bucket(app=firebase_app, name='dark-material-yz13.appspot.com')