# Python Cryptography Algorithms - Data Encryption

This project demonstrates the implementation of various cryptographic algorithms, including AES, DES, ECC, and Blowfish, using Python. A sample dataset (`amazon.csv`) is encrypted using each algorithm, and the encryption performance, including average time per row and total encryption time, is recorded.

The encrypted data is stored in a binary file (`encrypted_data.bin`). Additionally, the public and private keys for the ECC algorithm are generated and stored as `public_key.pem` and `private_key.pem`.

## Project Structure

- **Dataset**: `amazon.csv` (Sample dataset used for encryption)
- **Encrypted Data**: `encrypted_data.bin` (Stores the encrypted data in binary format)
- **Keys**: 
  - `public_key.pem` (ECC public key)
  - `private_key.pem` (ECC private key)

## Cryptographic Algorithms Implemented:
- **AES** (Advanced Encryption Standard)
- **DES** (Data Encryption Standard)
- **ECC** (Elliptic Curve Cryptography)
- **Blowfish**

## Features
- Implements encryption using AES, DES, ECC, and Blowfish algorithms.
- Measures and calculates:
  - Average encryption time per row.
  - Total time taken to encrypt the dataset.
- Encrypted data is saved in a binary file for secure storage.

## How to Run the Algorithms

Each algorithm has its own Python file. You can run an algorithm by using the following command in your terminal:

```bash
python <algorithm_file.py>
```

Example (Running ECC Encryption):

```bash
python ecc.py
```

## Files
- `aes.py`: AES encryption implementation.
- `des.py`: DES encryption implementation.
- `ecc.py`: ECC encryption implementation.
- `blowfish.py`: Blowfish encryption implementation.

## Prerequisites

To run the project, you need to have Python installed on your system along with the following libraries:

```bash
pip install pycryptodome cryptography
```

## Sample Dataset

The sample dataset used in this project is `amazon.csv`. You can replace this file with any CSV dataset of your choice to test encryption on different data.

## Performance Metrics

For each algorithm, the project calculates and displays:
- **Average Time per Row**: The average time taken to encrypt each row of the dataset.
- **Total Encryption Time**: The total time taken to encrypt the entire dataset.

## Usage Notes

- The encrypted data is stored in the `encrypted_data.bin` file. This file is in binary format for secure data handling.
- Public and private keys generated during ECC encryption are saved in `public_key.pem` and `private_key.pem`, respectively.
