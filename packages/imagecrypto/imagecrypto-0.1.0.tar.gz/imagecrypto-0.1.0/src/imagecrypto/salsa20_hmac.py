import cv2
import numpy as np
import time
import os
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms
from Crypto.Cipher import Salsa20
from cryptography.hazmat.backends import default_backend
def generate_ecdh_key():
    return ec.generate_private_key(ec.SECP256R1())

def compute_shared_key(private_key, peer_public_key):
    shared_key = private_key.exchange(ec.ECDH(), peer_public_key)
    return HKDF(
        algorithm=hashes.SHA256(),
        length=64,  # 32 bytes for Salsa20, 32 bytes for HMAC
        salt=None,
        info=b'handshake data',
    ).derive(shared_key)

def create_mac(key, data):
    h = hmac.HMAC(key, hashes.SHA256())
    h.update(data)
    return h.finalize()

def verify_mac(key, data, mac):
    h = hmac.HMAC(key, hashes.SHA256())
    h.update(data)
    try:
        h.verify(mac)
        return True
    except:
        return False

def encrypt_image(image_path, ecdh_private_key, ecdh_public_key):
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Error reading image from {image_path}")

    height, width, channels = img.shape
    start_time = time.time()
    shared_keys = compute_shared_key(ecdh_private_key, ecdh_public_key)
    encryption_key, mac_key = shared_keys[:32], shared_keys[32:]
    flattened = img.reshape(-1)
    cipher = Salsa20.new(key=encryption_key)
    nonce = cipher.nonce
    encrypted_data = cipher.encrypt(flattened.tobytes())
    mac = create_mac(mac_key, encrypted_data)
    encrypted_image = np.frombuffer(encrypted_data, dtype=np.uint8).reshape((height, width, channels))
    encryption_time = (time.time() - start_time) * 1000
    return img, encrypted_image, nonce, mac, (height, width, channels), encryption_time

def decrypt_image(encrypted_image, nonce, mac, shape, ecdh_private_key, ecdh_public_key):
    start_time = time.time()
    shared_keys = compute_shared_key(ecdh_private_key, ecdh_public_key)
    encryption_key, mac_key = shared_keys[:32], shared_keys[32:]
    flattened = encrypted_image.reshape(-1)
    if not verify_mac(mac_key, flattened.tobytes(), mac):
        raise ValueError("MAC verification failed")
    cipher = Salsa20.new(key=encryption_key, nonce=nonce)
    decrypted_data = cipher.decrypt(flattened.tobytes())
    decrypted_image = np.frombuffer(decrypted_data, dtype=np.uint8).reshape(shape)
    decryption_time = (time.time() - start_time) * 1000
    return decrypted_image, decryption_time

def get_images(image_path):
    ecdh_private_key = generate_ecdh_key()
    ecdh_public_key = ecdh_private_key.public_key()
    encrypted_image, encrypted_data, nonce, mac, shape, _ = encrypt_image(image_path, ecdh_private_key, ecdh_public_key)
    decrypted_image, _ = decrypt_image(encrypted_data, nonce, mac, shape, ecdh_private_key, ecdh_public_key)
    return encrypted_image, decrypted_image

def get_times(image_path):
    ecdh_private_key = generate_ecdh_key()
    ecdh_public_key = ecdh_private_key.public_key()
    _, encrypted_data, nonce, mac, shape, encryption_time = encrypt_image(image_path, ecdh_private_key, ecdh_public_key)
    _, decryption_time = decrypt_image(encrypted_data, nonce, mac, shape, ecdh_private_key, ecdh_public_key)
    return encryption_time, decryption_time