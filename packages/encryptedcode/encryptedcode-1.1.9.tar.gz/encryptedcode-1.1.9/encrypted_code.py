# Imports
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import os

mapping = {
    "a": "1", "b": "2", "c": "3", "d": "4", "e": "5", "f": "6", "g": "7", "h": "8", "i": "9", "j": "0",
    "k": "!", "l": "@", "m": "#", "n": "$", "o": "%", "p": "^", "q": "&", "r": "*", "s": "(", "t": ")",
    "u": "-", "v": "+", "w": "=", "x": "{", "y": "}", "z": "[", "A": "]", "B": ";", "C": ":", "D": ",",
    "E": ".", "F": "<", "G": ">", "H": "/", "I": "?", "J": "|", "K": "a", "L": "b", "M": "c", "N": "d",
    "O": "e", "P": "f", "Q": "g", "R": "h", "S": "i", "T": "j", "U": "k", "V": "l", "W": "m", "X": "n",
    "Y": "o", "Z": "p", "0": "q", "1": "r", "2": "s", "3": "t", "4": "u", "5": "v", "6": "w", "7": "x",
    "8": "y", "9": "z", "!": "A", "@": "B", "#": "C", "$": "D", "%": "E", "^": "F", "&": "G", "*": "H",
    "(": "I", ")": "J", "-": "K", "+": "L", "=": "M", "{": "N", "}": "O", "[": "P", "]": "Q", ";": "R",
    ":": "S", ",": "T", ".": "U", "<": "V", ">": "W", "/": "X", "?": "Y", "|": "Z"
}

def generate_key():
    return os.urandom(32)

def aes_encrypt(plaintext, key):
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(plaintext.encode()) + padder.finalize()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    return iv + ciphertext

def aes_decrypt(ciphertext, key):
    iv = ciphertext[:16]
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    padded_plaintext = decryptor.update(ciphertext[16:]) + decryptor.finalize()
    plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
    return plaintext.decode()

def encode(cadena, key):
    encrypted_cadena = aes_encrypt(cadena, key)
    xor_cadena = encrypted_cadena.hex()
    nueva_cadena = ""
    for caracter in xor_cadena:
        if caracter in mapping:
            nueva_cadena += mapping[caracter]
        else:
            nueva_cadena += caracter
    return nueva_cadena

def decode(cadena, key):
    map_inv = {v: k for k, v in mapping.items()}
    xor_cadena = ""
    for caracter in cadena:
        if caracter in map_inv:
            xor_cadena += map_inv[caracter]
        else:
            xor_cadena += caracter
    encrypted_cadena = bytes.fromhex(xor_cadena)
    decrypted_cadena = aes_decrypt(encrypted_cadena, key)
    return decrypted_cadena