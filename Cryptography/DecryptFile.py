from cryptography.fernet import Fernet

# Load the encryption key from the file
with open("encryption_key.txt", "rb") as file:
    key = file.read()

# Initialize Fernet with the key
fernet = Fernet(key)

# List of encrypted files
encrypted_files = ["e_system.txt", "e_clipboard.txt", "e_keys_logged.txt"]

# Decrypt each file
for encrypted_file in encrypted_files:
    with open(encrypted_file, 'rb') as file:
        encrypted_data = file.read()

    # Decrypt the data
    decrypted_data = fernet.decrypt(encrypted_data)

    # Write the decrypted data back to the file
    with open(encrypted_file, 'wb') as file:
        file.write(decrypted_data)

    print(f"Decrypted {encrypted_file}")

print("All files decrypted successfully")
