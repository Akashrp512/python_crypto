from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
import os
import csv
import time

key = b'Sixteen byte key'
iv = os.urandom(8)
cipher = Cipher(algorithms.Blowfish(key), modes.CBC(iv))

# Open the CSV file and read each row
with open('amazon.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    encryption_times = []
    for row in reader:
        # Encrypt each row using the Blowfish algorithm
        message = ','.join(row).encode()
        padder = padding.PKCS7(64).padder()
        padded_data = padder.update(message) + padder.finalize()
        encryptor = cipher.encryptor()

        # Start the timer
        start_time = time.time()

        ciphertext = encryptor.update(padded_data) + encryptor.finalize()

        # End the timer and append the encryption time to the list
        end_time = time.time()
        encryption_time = end_time - start_time
        encryption_times.append(encryption_time)

        print("Encrypted message: ", ciphertext)
        # Store the encrypted data in a binary file
        encrypted_file = open('encrypted_data.bin', 'wb')
        encrypted_file.write(ciphertext)
        encrypted_file.close()

    # Calculate and print the average and total encryption times
    avg_time = sum(encryption_times) / len(encryption_times)
    total_time = sum(encryption_times)
    print("Average encryption time per row:", avg_time)
    print("Total encryption time:", total_time)
