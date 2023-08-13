from dotenv import load_dotenv
import os
load_dotenv()
service = {
    "type": os.getenv('FIRIREBASE_TYPE'),
    "project_id": os.getenv('FIRIREBASE_PROJECT_ID'),
    "private_key_id": os.getenv('FIRIREBASE_PRIVATE_KEY_ID'),
    "private_key": os.getenv('FIRIREBASE_PRIVATE_KEY'),
    "client_email": os.getenv('FIRIREBASE_CLIENT_EMAIL'),
    "client_id": os.getenv('FIRIREBASE_CLIENT_ID'),
    "auth_uri": os.getenv('FIRIREBASE_AUTH_URI'),
    "token_uri": os.getenv('FIRIREBASE_TOKEN_URI'),
    "auth_provider_x509_cert_url": os.getenv('FIRIREBASE_AUTH_PROVIDER_X509_CERT_URL'),
    "client_x509_cert_url": os.getenv('FIRIREBASE_CLIENT_X509_CERT_URL'),
    "universe_domain": os.getenv('FIRIREBASE_UNIVERSE_DOMAIN')
}