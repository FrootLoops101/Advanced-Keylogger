from cryptography.fernet import Fernet
import os
print("Current Working Directory:", os.getcwd())

# Generate a key for encryption
key = Fernet.generate_key()
print("Encryption key generated:", key)

# Write the key to a file
with open("encryption_key.txt", "wb") as file:
    file.write(key)
print("Encryption key saved to encryption_key.txt")
