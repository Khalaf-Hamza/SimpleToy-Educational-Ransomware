import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


def decrypt_file(file_path, private_key):
    # Decrypt file using RSA private key and AES-GCM, then remove '.lolo' extension
    with open(file_path, 'rb') as file:
        encrypted_symmetric_key = file.read(256) 
        iv = file.read(16) 
        tag = file.read(16) 
        ciphertext = file.read()
    
    symmetric_key = private_key.decrypt(encrypted_symmetric_key, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
    cipher = Cipher(algorithms.AES(symmetric_key), modes.GCM(iv, tag))
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()
    with open(file_path, 'wb') as file:
        file.write(decrypted_data)
    os.rename(f'{file_path}',f'{file_path.strip(".lolo")}')
