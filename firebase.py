from firebase_admin import firestore_async, auth, credentials, initialize_app, storage

cred = credentials.Certificate(cert='service.json')
firebase_app = initialize_app(cred)
db = firestore_async.client(app=firebase_app)
auth = auth.Client(app=firebase_app)

storage = storage.bucket(app=firebase_app, name='dark-material-yz13.appspot.com')