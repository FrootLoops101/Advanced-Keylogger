# **Stealth Keylogger with Remote Email Reporting**

Welcome to the Stealth Keylogger with Remote Email Reporting project! This Python-based keylogger operates covertly in the background, capturing keyboard inputs, taking screenshots, recording audio, encrypting logs, and sending them to a designated email address.

## **DISCLAIMER:** 
This keylogger is intended for educational purposes only. Misuse of this software for unauthorized access or any illegal activities is prohibited. The author assumes no liability for any unethical or unlawful use of this tool.

## **Table of Contents**

- Features
- Prerequisites
- Setup
- Running the Keylogger
- Decrypting Encrypted Files
- Key Features
  - Keylogging
  - Computer Information
  - Clipboard Monitoring
  - Audio Recording
  - Screenshots
  - Encryption
  - Email Reporting
  - Frequency
- Troubleshooting
- Conclusion

## **Features**

- Keylogging: Captures keyboard inputs silently and logs them to key_log.txt.

- Computer Information: Gathers system details (hostname, IP addresses, processor information) and saves them in systeminfo.txt.

- Clipboard Monitoring: Records clipboard contents and saves them in clipboard.txt.

- Audio Recording: Records audio from the system's microphone for a specified duration (default: 10 seconds) and saves it as audio.wav.

- Screenshots: Periodically captures screenshots of the entire screen and saves them as ss.png.

- Encryption: Encrypts sensitive logs (system information, clipboard contents, key logs) using Fernet encryption before sending them via email. Encrypted files include e_system.txt.enc, e_clipboard.txt.enc, e_keys_logged.txt.enc.

- Email Reporting: Sends encrypted logs to a specified email address (toaddr). Modify toaddr as needed.

- Frequency: Adjusts reporting frequency (time_iteration) for sending logs via email.

## **Prerequisites**

Ensure Python (version 3.x) is installed on your system. Install the required libraries using pip:

    pip install pynput sounddevice cryptography Pillow

## **Setup**

- Download the Project: Clone or download this repository to your local machine.

- Setup Email Credentials: Open keylogger.py in your preferred IDE or text editor. Modify email_address and password to your email provider's credentials.

## **Running the Keylogger**

- Execute keylogger.py on the target system to initiate the keylogging process.

- python keylogger.py

## **Decrypting Encrypted Files**

- After collecting logs, encrypted files (e_system.txt.enc, e_clipboard.txt.enc, e_keys_logged.txt.enc) are created. Use decrypt_files.py to decrypt them:

        python decrypt_files.py

- Ensure encryption_key.txt is present in the directory to decrypt the files successfully.

## **Key Features**

**Keylogging**

- Captures keyboard inputs silently and logs them to key_log.txt.

**Computer Information**

- Gathers system details (hostname, IP addresses, processor information) and saves them in systeminfo.txt.

**Clipboard Monitoring**

- Records clipboard contents and saves them in clipboard.txt.

**Audio Recording**

- Records audio from the system's microphone for a specified duration (default: 10 seconds) and saves it as audio.wav.

**Screenshots**

- Periodically captures screenshots of the entire screen and saves them as ss.png.

**Encryption**

- Encrypts sensitive logs (system information, clipboard contents, key logs) using Fernet encryption before sending them via email.

**Email Reporting**

- Sends encrypted logs to a specified email address (toaddr). Modify toaddr as needed.

**Frequency**

- Adjusts reporting frequency (time_iteration) for sending logs via email.

## **Troubleshooting**

- Email Reporting Failures

        Ensure correct email credentials are configured. Address any login issues or two-factor authentication requirements.

- Data Retrieval Issues

        Grant necessary permissions for clipboard access, microphone usage, and screenshot capabilities.

- Antivirus Detection

        Some antivirus software may flag keyloggers as potentially malicious. Use responsibly and consider whitelisting the keylogger if necessary.

- Keylogger Not Working

        Check for syntax errors in the code and handle any runtime exceptions.

## **Conclusion**

The Stealth Keylogger with Remote Email Reporting is a valuable educational tool for understanding cybersecurity principles. Use it responsibly and adhere to legal guidelines and ethical standards. Respect user privacy and only deploy with explicit consent or for educational purposes. By fostering awareness of cybersecurity risks, this tool contributes to a safer digital environment.
