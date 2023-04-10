
import time
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.padding import PKCS7
from cryptography.hazmat.primitives.ciphers import modes, algorithms
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.ciphers import modes
from Crypto.Cipher import Blowfish
from Crypto import Random
import os
import csv


# Generate an elliptic curve private key
private_key = ec.generate_private_key(ec.SECP256R1())

# Get the public key associated with the private key
public_key = private_key.public_key()


# AES encryption function
def aes_encrypt(message, key, nonce):
    aesgcm = AESGCM(key)
    ciphertext = aesgcm.encrypt(
        nonce,
        message,
        None
    )
    return ciphertext


# ECC encryption function
def ecc_encrypt(message, private_key, public_key):
    shared_secret = private_key.exchange(ec.ECDH(), public_key)
    derived_key = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b'handshake data',
    ).derive(shared_secret)
    nonce = os.urandom(12)
    ciphertext = aes_encrypt(message, derived_key, nonce)
    return ciphertext


# Triple DES encryption function
def triple_des_encrypt(message, key, iv):
    cipher = Cipher(algorithms.TripleDES(
        key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    padder = PKCS7(64).padder()
    padded_message = padder.update(message) + padder.finalize()
    ciphertext = encryptor.update(padded_message) + encryptor.finalize()
    return ciphertext


# Blowfish encryption function
def blowfish_encrypt(message, key):
    iv = Random.new().read(Blowfish.block_size)
    cipher = Blowfish.new(key, Blowfish.MODE_CBC, iv)
    padder = PKCS7(64).padder()
    padded_message = padder.update(message) + padder.finalize()
    ciphertext = iv + cipher.encrypt(padded_message)
    return ciphertext


# Open the CSV file and read each row
with open('amazon.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)

    # AES encryption time
    start_time = time.time()
    for row in reader:
        message = ','.join(row).encode()
        ciphertext = aes_encrypt(message, aes_key)
        # Store the encrypted data in a binary file
        encrypted_file = open('encrypted_data/aes_encrypted_data.bin', 'ab')
        encrypted_file.write(ciphertext)
        encrypted_file.close()
    aes_encryption_time = time.time() - start_time
    print("AES encryption time: ", aes_encryption_time)

    # ECC encryption time
    start_time = time.time()
    for row in reader:
        message = ','.join(row).encode()
        ciphertext = ecc_encrypt(message)
        # Store the encrypted data in a binary file
        encrypted_file = open('encrypted_data/ecc_encrypted_data.bin', 'ab')
        encrypted_file.write(ciphertext)
        encrypted_file.close()
    ecc_encryption_time = time.time() - start_time
    print("ECC encryption time: ", ecc_encryption_time)

    # Triple DES encryption time
    start_time = time.time()
    for row in reader:
        message = ','.join(row).encode()
        ciphertext = triple_des_encrypt(message, triple_des_key)
        # Store the encrypted data in a binary file
        encrypted_file = open(
            'encrypted_data/triple_des_encrypted_data.bin', 'ab')
        encrypted_file.write(ciphertext)
        encrypted_file.close()
    triple_des_encryption_time = time.time() - start_time
    print("Triple DES encryption time: ", triple_des_encryption_time)

    # Blowfish encryption time
    start_time = time.time()
    for row in reader:
        message = ','.join(row).encode()
        ciphertext = blowfish_encrypt(message, blowfish_key)
        # Store the encrypted data in a binary file
        encrypted_file = open(
            'encrypted_data/blowfish_encrypted_data.bin', 'ab')
        encrypted_file.write(ciphertext)
        encrypted_file.close()
    blowfish_encryption_time = time.time() - start_time
    print("Blowfish encryption time: ", blowfish_encryption_time)
