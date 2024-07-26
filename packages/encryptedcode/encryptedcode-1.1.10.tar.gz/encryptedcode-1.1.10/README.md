<h1>Encrypted Code - L0123 Algorithm</h1>

### About
EncryptedCode is a python library accessible to everyone that is under improvements where I use a new encryption algorithm created by &copy; Software Engineer <a href="https://leoglez.vercel.app/">Leandro Gonzalez Espinosa.</a> and named L0123.

## INSTALATION
``` bash
pip install encryptedcode
```
## IMPORTANT
 REMEMBER SAVE THE KEY INSIDE TO ENVIROMENT VARIABLE FOR YOUR SECURITY

### USAGE EXAMPLE
```python
#imports
from encryptedcode import generate_key, encode, decode

# Generate a key
key = generate_key()

# Encode a string
encoded_string = encode("your_password", key)
print(f"Encoded: {encoded_string}")

# Decode the string
decoded_string = decode(encoded_string, key)
print(f"Decoded: {decoded_string}")
```