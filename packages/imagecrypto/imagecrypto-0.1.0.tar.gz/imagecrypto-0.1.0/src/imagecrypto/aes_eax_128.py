import cv2
import numpy as np
import time
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from Crypto.Cipher import AES
def generate_ecdhe_key():
    return ec.generate_private_key(ec.SECP256R1())

def compute_shared_key(private_key, peer_public_key):
    shared_key = private_key.exchange(ec.ECDH(), peer_public_key)
    return HKDF(
        algorithm=hashes.SHA256(),
        length=16,
        salt=None,
        info=b'handshake data',
    ).derive(shared_key)

def encrypt_image(image_path, ecdhe_private_key, ecdhe_public_key):
    img = cv2.imread(image_path)
    height, width, channels = img.shape
    start_time = time.time()
    shared_key = compute_shared_key(ecdhe_private_key, ecdhe_public_key)
    flattened = img.reshape(-1)
    cipher = AES.new(shared_key, AES.MODE_EAX)
    nonce = cipher.nonce
    encrypted_data, tag = cipher.encrypt_and_digest(flattened.tobytes())
    encrypted_image = np.frombuffer(encrypted_data, dtype=np.uint8)[:height*width*channels].reshape((height, width, channels))
    encryption_time = (time.time() - start_time) * 1000
    return encrypted_image, encrypted_data, nonce, tag, (height, width, channels), encryption_time

def decrypt_image(encrypted_data, nonce, tag, shape, ecdhe_private_key, ecdhe_public_key):
    start_time = time.time()
    shared_key = compute_shared_key(ecdhe_private_key, ecdhe_public_key)
    cipher = AES.new(shared_key, AES.MODE_EAX, nonce=nonce)
    decrypted_data = cipher.decrypt_and_verify(encrypted_data, tag)
    decrypted_image = np.frombuffer(decrypted_data, dtype=np.uint8).reshape(shape)
    decryption_time = (time.time() - start_time) * 1000
    return decrypted_image, decryption_time

def get_images(image_path):
    ecdhe_private_key = generate_ecdhe_key()
    ecdhe_public_key = ecdhe_private_key.public_key()
    encrypted_image, encrypted_data, nonce, tag, shape, _ = encrypt_image(image_path, ecdhe_private_key, ecdhe_public_key)
    decrypted_image, _ = decrypt_image(encrypted_data, nonce, tag, shape, ecdhe_private_key, ecdhe_public_key)
    return encrypted_image, decrypted_image

def get_times(image_path):
    ecdhe_private_key = generate_ecdhe_key()
    ecdhe_public_key = ecdhe_private_key.public_key()
    # Capture all returned values from encrypt_image

    _, encrypted_data, nonce, tag, shape, encryption_time = encrypt_image(image_path, ecdhe_private_key, ecdhe_public_key)
    _, decryption_time = decrypt_image(encrypted_data, nonce, tag, shape, ecdhe_private_key, ecdhe_public_key)
    return encryption_time, decryption_time