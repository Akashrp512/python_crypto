from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import os
import csv
import time

# Generate a password to derive a key from
password = b"mysecretpassword"

# Derive a 256-bit key from the password using PBKDF2
salt = os.urandom(16)
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=100000,
    backend=default_backend()
)
key = kdf.derive(password)

# Generate a random IV (nonce)
iv = os.urandom(16)

total_encryption_time = 0
num_rows = 0

# Open the CSV file and read each row
with open('amazon.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    for row in reader:
        # Encrypt each row using AES-GCM
        message = ','.join(row).encode()

        # Start the timer
        start_time = time.time()

        cipher = Cipher(algorithms.AES(key), modes.GCM(iv),
                        backend=default_backend())
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(message) + encryptor.finalize()
        tag = encryptor.tag

        # End the timer and calculate the encryption time
        end_time = time.time()
        encryption_time = end_time - start_time

        # Update the total encryption time and the number of rows encrypted
        total_encryption_time += encryption_time
        num_rows += 1

        print("Encryption time for row", num_rows, ":", encryption_time)
        print("Encrypted message: ", ciphertext)
        print("Authentication tag: ", tag)

        # Store the encrypted data and the nonce in a binary file
        encrypted_file = open('encrypted_data.bin', 'ab')
        encrypted_file.write(iv)
        encrypted_file.write(tag)
        encrypted_file.write(ciphertext)
        encrypted_file.close()

# Calculate the average encryption time
average_encryption_time = total_encryption_time / num_rows
print("Average encryption time:", average_encryption_time)

# Calculate the total encryption time for all rows
print("Total encryption time:", total_encryption_time)
