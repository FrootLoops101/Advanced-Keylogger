from cryptography.fernet import Fernet

Key = Fernet.generate_key()
file = open("encryption_key.txt", "wb")
file.write(Key)
file.close()