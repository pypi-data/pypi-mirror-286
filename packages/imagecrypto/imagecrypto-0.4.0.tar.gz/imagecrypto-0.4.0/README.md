# 🔐 ImageCrypto

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Versions](https://img.shields.io/pypi/pyversions/imagecrypto.svg)](https://pypi.org/project/imagecrypto/)

ImageCrypto is a powerful and easy-to-use Python package for secure image encryption using various symmetric ciphers with asymmetric Elliptic Curve Cryptography (ECC) for key generation.

## 🌟 Features & Available Modules

ImageCrypto offers multiple symmetric encryption algorithms, each implemented as a separate module:

* `aes_gcm_128`: AES-128 in GCM mode
* `aes_ccm_128`: AES-128 in CCM mode
* `aes_gcm_256`: AES-256 in GCM mode
* `aes_eax_128`: AES-128 in EAX mode
* `chacha20_poly1305`: ChaCha20-Poly1305
* `salsa20`: Salsa20

Key features:

* Secure key generation using asymmetric ECC (SECP256R1 curve)
* Fast symmetric encryption
* Easy-to-use API
* Performance metrics (encryption time)
* Visualization of original and encrypted images

Each module provides the same API:

* `get_encrypted_image(image_path)`: Encrypts the image and returns the encrypted image data
* `get_encryption_time(image_path)`: Returns encryption time
* `display_images(original_path, encrypted_image)`: Displays the original and encrypted images

This consistent API across all encryption algorithms allows for easy comparison and flexibility in choosing the most suitable method for your needs.

## 🚀 Installation
Install ImageCrypto using pip:
```bash
pip install imagecrypto
```
## 📝 Usage Example

Here's an example of how to use ImageCrypto and display the results:

```python
from imagecrypto import aes_gcm_256
import matplotlib.pyplot as plt

# Define the path for your original image
original_image = "path/to/your/image.jpg"

# Encrypt an image
encrypted_image = aes_gcm_256.get_encrypted_image(original_image)

# Get encryption time
encrypt_time = aes_gcm_256.get_encryption_time(original_image)
print(f"Encryption time: {encrypt_time:.2f} ms")

# Display the original and encrypted images
aes_gcm_256.display_images(original_image, encrypted_image)
```

### Inputs
* Path to an original image file (JPEG, PNG, etc.)

### Outputs
* Encrypted image data
* Encryption time (in milliseconds)
* Visual display of original and encrypted images

## 🛠️ Dependencies
* OpenCV (cv2)
* cryptography
* pycryptodome
* numpy
* matplotlib

## 📄 License
ImageCrypto is released under the MIT License.

## 📧 Contact
Project Link: [https://github.com/nidhi-bhatt/imagecrypto](https://github.com/nidhi-bhatt/imagecrypto)

---
Made with ❤️ by Nidhi