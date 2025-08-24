from dotenv import load_dotenv
import os

load_dotenv()

email = os.getenv("WELLFOUND_EMAIL")
password = os.getenv("WELLFOUND_PASSWORD")

print("Email:", email)
print("Password:", password)
