import cv2
import numpy as np
import time
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers.aead import AESCCM
import matplotlib.pyplot as plt

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
    if img is None:
        raise ValueError(f"Error reading image from {image_path}")

    height, width, channels = img.shape
    start_time = time.time()
    shared_key = compute_shared_key(ecdhe_private_key, ecdhe_public_key)
    flattened = img.reshape(-1)
    aesccm = AESCCM(shared_key)
    nonce = os.urandom(12)  # AESCCM requires a nonce of at least 7 bytes and at most 13 bytes
    encrypted_data = aesccm.encrypt(nonce, flattened.tobytes(), None)
    encrypted_image = np.frombuffer(encrypted_data, dtype=np.uint8)[:height*width*channels].reshape((height, width, channels))
    encryption_time = (time.time() - start_time) * 1000
    return encrypted_image, encrypted_data, nonce, (height, width, channels), encryption_time

def decrypt_image(encrypted_data, nonce, shape, ecdhe_private_key, ecdhe_public_key):
    start_time = time.time()
    shared_key = compute_shared_key(ecdhe_private_key, ecdhe_public_key)
    aesccm = AESCCM(shared_key)
    decrypted_data = aesccm.decrypt(nonce, encrypted_data, None)
    decrypted_image = np.frombuffer(decrypted_data, dtype=np.uint8).reshape(shape)
    decryption_time = (time.time() - start_time) * 1000
    return decrypted_image, decryption_time

def save_image(image, filename):
    cv2.imwrite(filename, image)

def get_images(image_path, encrypted_path, decrypted_path):
    ecdhe_private_key = generate_ecdhe_key()
    ecdhe_public_key = ecdhe_private_key.public_key()
    encrypted_image, encrypted_data, nonce, shape, _ = encrypt_image(image_path, ecdhe_private_key, ecdhe_public_key)
    save_image(encrypted_image, encrypted_path)
    decrypted_image, _ = decrypt_image(encrypted_data, nonce, shape, ecdhe_private_key, ecdhe_public_key)
    save_image(decrypted_image, decrypted_path)
    return encrypted_path, decrypted_path

def get_times(image_path):
    ecdhe_private_key = generate_ecdhe_key()
    ecdhe_public_key = ecdhe_private_key.public_key()
    _, encrypted_data, nonce, shape, encryption_time = encrypt_image(image_path, ecdhe_private_key, ecdhe_public_key)
    _, decryption_time = decrypt_image(encrypted_data, nonce, shape, ecdhe_private_key, ecdhe_public_key)
    return encryption_time, decryption_time

def display_images(original_path, encrypted_path, decrypted_path):
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle('AES-CCM-128 Encryption/Decryption', fontsize=16)

    ax1.imshow(cv2.cvtColor(cv2.imread(original_path), cv2.COLOR_BGR2RGB))
    ax1.set_title('Original')
    ax1.axis('off')

    ax2.imshow(cv2.cvtColor(cv2.imread(encrypted_path), cv2.COLOR_BGR2RGB))
    ax2.set_title('Encrypted')
    ax2.axis('off')

    ax3.imshow(cv2.cvtColor(cv2.imread(decrypted_path), cv2.COLOR_BGR2RGB))
    ax3.set_title('Decrypted')
    ax3.axis('off')

    plt.tight_layout()
    plt.show()