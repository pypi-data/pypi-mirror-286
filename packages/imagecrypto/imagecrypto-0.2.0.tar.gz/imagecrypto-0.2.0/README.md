# 🔐 ImageCrypto

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

ImageCrypto is a powerful and easy-to-use Python package for secure image encryption and decryption.

## 🌟 Features & Available Modules

ImageCrypto offers multiple encryption algorithms, each implemented as a separate module:

* `aes_gcm_128`: AES-128 in GCM mode
* `aes_ccm_128`: AES-128 in CCM mode
* `aes_gcm_256`: AES-256 in GCM mode
* `aes_eax_128`: AES-128 in EAX mode
* `chacha20_poly1305`: ChaCha20-Poly1305
* `salsa20_hmac`: Salsa20 with HMAC

Key features:
- Secure key exchange using ECDHE
- Fast encryption and decryption
- Easy-to-use API
- Performance metrics (encryption and decryption times)

Each module provides the same API:
* `get_images(image_path)`: Returns encrypted and decrypted images
* `get_times(image_path)`: Returns encryption and decryption times

This consistent API across all encryption algorithms allows for easy comparison and flexibility in choosing the most suitable method for your needs.

## 🚀 Installation
Install ImageCrypto using pip:
```bash
pip install imagecrypto
```

## 📚 Usage
Here's an example of how to use ImageCrypto and display the results:

```
from imagecrypto import aes_gcm_256
import matplotlib.pyplot as plt

# Define the path to your original image
original_image = "path/to/your/image.jpg"

# Encrypt and decrypt an image
encrypted_image, decrypted_image = aes_gcm_256.get_images(original_image)

# Get encryption and decryption times
encrypt_time, decrypt_time = aes_gcm_256.get_times(original_image)
print(f"Encryption time: {encrypt_time:.2f} ms")
print(f"Decryption time: {decrypt_time:.2f} ms")

# Save encrypted and decrypted images
cv2.imwrite(f"encrypted.png", encrypted_image)
cv2.imwrite(f"decrypted.png", decrypted_image)

```
## Inputs
* Path to an image file (JPEG, PNG, etc.)

## Outputs
* Encrypted image
* Decrypted image
* Encryption time (in milliseconds)
* Decryption time (in milliseconds)

## 🛠️ Dependencies
* Pillow
* cryptography
* crypto
* pycryptodome
* numpy
* matplotlib


## 📄 License
ImageCrypto is released under the MIT License.

---
Made with ❤️ by Nidhi