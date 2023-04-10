from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os
import csv
import time

# Generate an elliptic curve private key
private_key = ec.generate_private_key(ec.SECP256R1())

# Serialize the private key to PEM format and write it to a file
with open("private_key.pem", "wb") as f:
    f.write(private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ))

# Get the public key associated with the private key
public_key = private_key.public_key()

# Open the CSV file and read each row
with open('amazon.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    total_encryption_time = 0
    rows_processed = 0
    for row in reader:
        # Encrypt each row using the ECC algorithm
        message = ','.join(row).encode()

        # Start the timer
        start_time = time.time()

        shared_secret = private_key.exchange(ec.ECDH(), public_key)
        derived_key = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=b'handshake data',
        ).derive(shared_secret)
        nonce = os.urandom(12)
        aesgcm = AESGCM(derived_key)
        ciphertext = aesgcm.encrypt(
            nonce,
            message,
            None
        )

        # End the timer and calculate the encryption time
        end_time = time.time()
        encryption_time = end_time - start_time
        total_encryption_time += encryption_time
        rows_processed += 1
        print("Encryption time:", encryption_time)

        print("Encrypted message: ", ciphertext)
        # Store the encrypted data in a binary file
        encrypted_file = open('encrypted_data.bin', 'wb')
        encrypted_file.write(ciphertext)
        encrypted_file.close()

    # Calculate the average encryption time and total time taken
    avg_encryption_time = total_encryption_time / rows_processed
    total_time_taken = total_encryption_time
    print("Average encryption time:", avg_encryption_time)
    print("Total time taken:", total_time_taken)
