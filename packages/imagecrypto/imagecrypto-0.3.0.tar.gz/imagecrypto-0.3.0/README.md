# 🔐 ImageCrypto

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Versions](https://img.shields.io/pypi/pyversions/imagecrypto.svg)](https://pypi.org/project/imagecrypto/)

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
- Visualization of original, encrypted, and decrypted images

Each module provides the same API:
* `get_images(image_path, encrypted_path, decrypted_path)`: Encrypts and decrypts the image, saves the results, and returns the paths
* `get_times(image_path)`: Returns encryption and decryption times
* `display_images(original_path, encrypted_path, decrypted_path)`: Displays the original, encrypted, and decrypted images

This consistent API across all encryption algorithms allows for easy comparison and flexibility in choosing the most suitable method for your needs.

## 🚀 Installation
Install ImageCrypto using pip:
```bash
pip install imagecrypto
```
## 📚 Usage

Here's an example of how to use ImageCrypto and display the results:

```python
from imagecrypto import aes_gcm_256
import matplotlib.pyplot as plt

# Define the paths for your images
original_image = "path/to/your/image.jpg"
encrypted_image = "path/to/save/encrypted.png"
decrypted_image = "path/to/save/decrypted.png"

# Encrypt and decrypt an image
encrypted_path, decrypted_path = aes_gcm_256.get_images(original_image, encrypted_image, decrypted_image)

# Get encryption and decryption times
encrypt_time, decrypt_time = aes_gcm_256.get_times(original_image)
print(f"Encryption time: {encrypt_time:.2f} ms")
print(f"Decryption time: {decrypt_time:.2f} ms")

# Display the original, encrypted, and decrypted images
aes_gcm_256.display_images(original_image, encrypted_path, decrypted_path)
```

### Inputs
* Path to an original image file (JPEG, PNG, etc.)
* Path to save the encrypted image
* Path to save the decrypted image

### Outputs
* Encrypted image (saved to specified path)
* Decrypted image (saved to specified path)
* Encryption time (in milliseconds)
* Decryption time (in milliseconds)
* Visual display of original, encrypted, and decrypted images

## 🛠️ Dependencies
* OpenCV (cv2)
* cryptography
* pycryptodome
* numpy
* matplotlib

## 📄 License
ImageCrypto is released under the MIT License.


## 📧 Contact


Project Link: [https://github.com/nidhi-bhatt/imagecrypto](https://github.com/nidh-bhatt/imagecrypto) 

---
Made with ❤️ by Nidhi