from cryptography.fernet import Fernet
from ..vars import Var
root_key = Var.root_key

def decrypt(key: str, data_to_decrypt: str) -> str:
    '''
    here key is the decryption key and data will be encrypted data
    '''
    try:
        key = Fernet(key)
        decrypted_datas = key.decrypt(data_to_decrypt.encode())
        return decrypted_datas.decode()
    except:
        return None

def encrypt(key: str, data_to_encrypt: str) -> str:
    '''
    here key is the decryption key and data will be text which needs to be decrypted
    '''
    try:
        key = Fernet(key)
        encrypted_data = key.encrypt(data_to_encrypt.encode())
        return encrypted_data.decode()
    except:
        return None

def create_new_key() -> str:
    '''
    this section is use to create a new key
    '''
    key = Fernet.generate_key()
    return key.decode()

