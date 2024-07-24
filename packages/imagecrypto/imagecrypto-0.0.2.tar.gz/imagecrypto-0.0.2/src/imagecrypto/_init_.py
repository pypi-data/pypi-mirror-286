from . import aes_gcm_128
from . import aes_ccm_128
from . import aes_gcm_256
from . import aes_eax_128
from . import chacha20_poly1305
from . import salsa20

__all__ = ['aes_gcm_128', 'aes_ccm_128', 'aes_gcm_256', 'aes_eax_128', 'chacha20_poly1305', 'salsa20']

# Version of the imagecrypto package
__version__ = "0.5.0"

# A brief description of the package
__description__ = """
ImageCrypto is a Python package for secure image encryption using various symmetric ciphers 
(AES-GCM, AES-CCM, AES-EAX, ChaCha20-Poly1305, Salsa20) with Elliptic Curve Cryptography (ECC) 
for key generation. It focuses on encryption without key exchange or decryption functionality.
"""

# The author of the package
__author__ = "Nidhi Bhatt"

# The author's email
__email__ = "itsnibhatt@gmail.com"

# The license under which the package is released
__license__ = "MIT"

# The package's documentation website
__url__ = "https://github.com/nidhi-bhatt/imagecrypto"