

import argparse
import cv2
from . import aes_gcm_128, aes_ccm_128, aes_gcm_256, aes_eax_128, chacha20_poly1305, salsa20_hmac


def main():
    parser = argparse.ArgumentParser(description="Image Crypto: Encrypt and decrypt images using various algorithms")
    parser.add_argument("image_path", help="Path to the input image")
    parser.add_argument("algorithm",
                        choices=["aes_gcm_128", "aes_ccm_128", "aes_gcm_256", "aes_eax_128", "chacha20_poly1305",
                                 "salsa20_hmac"], help="Encryption algorithm to use")
    parser.add_argument("--output", "-o", help="Path to save the encrypted image (default: encrypted_image.png)",
                        default="encrypted_image.png")
    parser.add_argument("--decrypt", "-d", help="Path to save the decrypted image (default: decrypted_image.png)",
                        default="decrypted_image.png")
    parser.add_argument("--times", "-t", action="store_true", help="Display encryption and decryption times")

    args = parser.parse_args()

    # Select the appropriate algorithm
    algorithms = {
        "aes_gcm_128": aes_gcm_128,
        "aes_ccm_128": aes_ccm_128,
        "aes_gcm_256": aes_gcm_256,
        "aes_eax_128": aes_eax_128,
        "chacha20_poly1305": chacha20_poly1305,
        "salsa20_hmac": salsa20_hmac
    }

    selected_algorithm = algorithms[args.algorithm]

    # Encrypt and decrypt the image
    encrypted_image, decrypted_image = selected_algorithm.get_images(args.image_path)

    # Save the encrypted and decrypted images
    cv2.imwrite(args.output, encrypted_image)
    cv2.imwrite(args.decrypt, decrypted_image)

    print(f"Encrypted image saved to: {args.output}")
    print(f"Decrypted image saved to: {args.decrypt}")

    # Display encryption and decryption times if requested
    if args.times:
        encryption_time, decryption_time = selected_algorithm.get_times(args.image_path)
        print(f"Encryption time: {encryption_time:.2f} ms")
        print(f"Decryption time: {decryption_time:.2f} ms")


if __name__ == "__main__":
    main()