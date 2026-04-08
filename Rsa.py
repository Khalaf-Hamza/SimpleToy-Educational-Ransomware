from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend

def generate_keys(key_size=2048):
    """
    Generate a pair of RSA private and public keys.

    Args:
        key_size (int, optional): The size of the RSA key to generate. Default is 2048 bits.

    Returns:
        tuple: A tuple containing the private key (bytes) and public key (bytes) in PEM format.

    Note:
        This function generates an RSA private key with the specified key size and derives the corresponding
        public key. It returns both keys in PEM format without encryption.
    """
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size,
        backend=default_backend()
    )

    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    public_pem = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    return private_pem, public_pem
