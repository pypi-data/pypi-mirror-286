from setuptools import setup, find_packages

# Read the requirements from requirements.txt
with open("requirements.txt") as f:
    required = f.read().splitlines()

setup(
    name="Cryptonit-BOT",
    version="0.1.2",
    description="A bot for encryption and decryption using Telegram",
    author="ruslanlap",  # Replace with your actual name
    author_email="your.email@example.com",  # Replace with your actual email
    url="https://github.com/ruslanlap/Cryptonit-BOT-COPYY",
    packages=find_packages(),
    install_requires=required,
)
