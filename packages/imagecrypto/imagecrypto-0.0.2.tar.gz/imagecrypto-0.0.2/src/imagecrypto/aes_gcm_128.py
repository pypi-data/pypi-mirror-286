import cv2
import numpy as np
import time
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import matplotlib.pyplot as plt


def generate_ecc_key():
    return ec.generate_private_key(ec.SECP256R1())


def encrypt_image(image_path):
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Error reading image from {image_path}")

    height, width, channels = img.shape
    start_time = time.time()

    # Generate ECC key
    private_key = generate_ecc_key()

    # Use the private key to derive an encryption key
    derived_key = HKDF(
        algorithm=hashes.SHA256(),
        length=16,
        salt=None,
        info=b'encryption',
    ).derive(private_key.private_numbers().private_value.to_bytes(32, 'big'))

    flattened = img.reshape(-1)
    aesgcm = AESGCM(derived_key)
    nonce = os.urandom(12)
    encrypted_data = aesgcm.encrypt(nonce, flattened.tobytes(), None)
    encrypted_image = np.frombuffer(encrypted_data, dtype=np.uint8)[:height * width * channels].reshape(
        (height, width, channels))
    encryption_time = (time.time() - start_time) * 1000
    return encrypted_image, encryption_time


def get_encrypted_image(image_path):
    encrypted_image, _ = encrypt_image(image_path)
    return encrypted_image


def get_encryption_time(image_path):
    _, encryption_time = encrypt_image(image_path)
    return encryption_time


def display_images(original_path, encrypted_image):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
    fig.suptitle('ECC-based AES-GCM-128 Encryption', fontsize=16)

    ax1.imshow(cv2.cvtColor(cv2.imread(original_path), cv2.COLOR_BGR2RGB))
    ax1.set_title('Original')
    ax1.axis('off')

    ax2.imshow(cv2.cvtColor(encrypted_image, cv2.COLOR_BGR2RGB))
    ax2.set_title('Encrypted')
    ax2.axis('off')

    plt.tight_layout()
    plt.show()