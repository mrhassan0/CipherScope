# CipherScope

Cryptography learning workbench for encryption, attack demonstrations, frequency analysis, and live performance comparison.

cd "/home/rakibul/Desktop/CSE721 Project"
python3 backend/app.py

This project follows the original `CSE721 Project requirements.pdf`.

It is a simple frontend/backend project with no database. The frontend collects input and shows results. The Python backend performs the cryptographic algorithms.

## How to Run

```bash
python3 backend/app.py
```

Then open:

```text
http://localhost:8000
```

## How to Test

```bash
python3 tests/test_algorithms.py
```

## Included Requirements

- Substitution cipher
- Caesar cipher brute-force attack demo
- Substitution frequency analysis
- Double transposition cipher
- Double transposition frequency analysis
- DES with auto-generated key and all round keys
- AES-128 with auto-generated key and all round keys
- RSA key generation, encryption, decryption, and factorization attack demo
- ECC point listing, private key, public key, and ECDH shared key
- Security and performance comparison table
- Live technical performance table for all six algorithms

## Feature PDF

A detailed feature document is available at:

```text
docs/CipherScope_Feature_Documentation.pdf
```

## Important Rule

The code does not use OpenSSL or built-in cryptographic libraries for the core algorithm operations. DES, AES, RSA, and ECC logic are written manually in Python for learning and demonstration.

## Folder Structure

```text
backend/
  app.py
  classical/
    substitution.py
    caesar_brute_force_attack.py
    double_transposition.py
  symmetric/
    des.py
    aes.py
  public_key/
    rsa.py
    ecc.py
  utils/
    frequency_analysis.py
    timing.py
  analysis/
    performance_comparison.py

frontend/
  index.html
  style.css
  script.js

tests/
  test_algorithms.py
```
