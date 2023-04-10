from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import os
import csv
import time

# Generate a password to derive a key from
password = b"mysecretpassword"

# Derive a 192-bit key from the password using PBKDF2
salt = os.urandom(16)
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=24,
    salt=salt,
    iterations=100000,
    backend=default_backend()
)
key = kdf.derive(password)

# Generate a random IV
iv = os.urandom(8)

# Initialize the variables to calculate the average encryption time
total_encryption_time = 0
num_encryptions = 0

# Open the CSV file and read each row
with open('amazon.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    for row in reader:
        # Encrypt each row using Triple DES
        message = ','.join(row).encode()

        # Start the timer
        start_time = time.time()

        cipher = Cipher(algorithms.TripleDES(key), modes.CFB(iv),
                        backend=default_backend())
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(message) + encryptor.finalize()

        # End the timer and calculate the encryption time
        end_time = time.time()
        encryption_time = end_time - start_time
        print("Encryption time:", encryption_time)

        # Add the encryption time to the total and increment the number of encryptions
        total_encryption_time += encryption_time
        num_encryptions += 1

        print("Encrypted message: ", ciphertext)
        # Store the encrypted data and the IV in a binary file
        encrypted_file = open('encrypted_data.bin', 'ab')
        encrypted_file.write(iv)
        encrypted_file.write(ciphertext)
        encrypted_file.close()

# Calculate the average encryption time and the total time taken for encryption
average_encryption_time = total_encryption_time / num_encryptions
print("Average encryption time per row:", average_encryption_time)
print("Total encryption time:", total_encryption_time)
