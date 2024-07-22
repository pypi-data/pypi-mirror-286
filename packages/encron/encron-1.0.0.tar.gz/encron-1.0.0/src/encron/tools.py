from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import os
import base64
import binascii

def encrypt_data(password, data):
    # Convert password to bytes and derive a key using PBKDF2
    password_bytes = password.encode()
    salt = os.urandom(16)  # Generate a random salt
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = kdf.derive(password_bytes)
    
    # Generate a random initialization vector (IV)
    iv = os.urandom(16)

    # Create a cipher object using the derived key and IV
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())

    # Create an encryptor object
    encryptor = cipher.encryptor()

    # Pad the data to make its length a multiple of the block size (16 bytes for AES)
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(data.encode()) + padder.finalize()

    # Encrypt the padded data
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

    # Return the salt, IV, and the encrypted data (salt and IV are needed for decryption)
    return base64.b64encode(salt + iv + encrypted_data).decode('utf-8')


def decrypt_data(password, encrypted_data):
    # Convert password to bytes
    password_bytes = password.encode()
    
    # Decode the base64 encoded encrypted data
    encrypted_data_bytes = base64.b64decode(encrypted_data.encode('utf-8'))
    
    # Extract the salt, IV, and encrypted data
    salt = encrypted_data_bytes[:16]
    iv = encrypted_data_bytes[16:32]
    encrypted_data = encrypted_data_bytes[32:]
    
    # Derive the key using the same PBKDF2 settings
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = kdf.derive(password_bytes)

    # Create a cipher object using the derived key and IV
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())

    # Create a decryptor object
    decryptor = cipher.decryptor()

    # Decrypt the data
    decrypted_padded_data = decryptor.update(encrypted_data) + decryptor.finalize()

    # Remove padding
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    decrypted_data = unpadder.update(decrypted_padded_data) + unpadder.finalize()

    return decrypted_data.decode('utf-8')
   
   
def find_file(filename):
    current_dir = os.getcwd()
    
    while True:
        potential_path = os.path.join(current_dir, filename)
        if os.path.isfile(potential_path):
            return potential_path
        
        # Move to the parent directory
        parent_dir = os.path.dirname(current_dir)
        if parent_dir == current_dir:  # This means we have reached the root directory
            break
        current_dir = parent_dir
    
    return 'File not found' 
    

def encrypt_file(file_path, password):
    file = find_file(file_path)
    if file == 'File not found':
        print(file)
        return
    
    with open(file, 'r') as file_obj:
        data = file_obj.read()
    encrypted_data = encrypt_data(password, data)
    with open(file, 'w') as file_obj:
        file_obj.write(encrypted_data)

def decrypt_file(file_path, password):
    file = find_file(file_path)
    if file == 'File not found':
        print(file)
        return
    
    with open(file, 'r') as file_obj:
        encrypted_data = file_obj.read()
    decrypted_data = decrypt_data(password, encrypted_data)
    
    with open(file, 'w') as file_obj:
        file_obj.write(decrypted_data)

def encrypt_web(password, data):
    password_bytes = password.encode()
    data_bytes = data.encode()

    salt = os.urandom(16)
    iv = os.urandom(12)

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = kdf.derive(password_bytes)

    cipher = Cipher(algorithms.AES(key), modes.GCM(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(data_bytes) + encryptor.finalize()
    tag = encryptor.tag

    encrypted_data_bytes = salt + iv + tag + encrypted_data
    encrypted_data_base64 = base64.urlsafe_b64encode(encrypted_data_bytes).decode('utf-8')
    
    return encrypted_data_base64



def decrypt_web(password, encrypted_data):
    #print(f"Encrypted data before padding: {encrypted_data}")
    
    # Convert password to bytes
    password_bytes = password.encode()
    
    # Add padding to the base64 string if necessary
    missing_padding = len(encrypted_data) % 4
    if missing_padding != 0:
        encrypted_data += '=' * (4 - missing_padding)
    
    #print(f"Encrypted data after padding: {encrypted_data}")
    
    # Decode the URL-safe Base64 encoded encrypted data
    try:
        encrypted_data_bytes = base64.urlsafe_b64decode(encrypted_data.encode('utf-8'))
    except binascii.Error as e:
        print(f"Error decoding base64: {e}")
        return False
    
    #print(f"Encrypted data bytes: {encrypted_data_bytes}")

    # Extract the salt, IV, tag, and encrypted data
    salt = encrypted_data_bytes[:16]
    iv = encrypted_data_bytes[16:28]
    tag = encrypted_data_bytes[28:44]
    encrypted_data = encrypted_data_bytes[44:]
    
    #print(f"Salt: {salt}, IV: {iv}, Tag: {tag}, Encrypted data: {encrypted_data}")

    # Derive the key using the same PBKDF2 settings
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = kdf.derive(password_bytes)

    # Create a cipher object using the derived key and IV
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag), backend=default_backend())

    # Create a decryptor object
    decryptor = cipher.decryptor()

    # Decrypt the data
    try:
        decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()
    except Exception as e:
        print(f"Error during decryption: {e}")
        return False

    return decrypted_data.decode('utf-8')

def check_web_enc(password, encrypted_data):
    try:
        return decrypt_web(password, encrypted_data)
    except Exception as e:
        print(f"Invalid decryption key: {e}")
        return False


