from setuptools import setup, find_packages

setup(
    name="Cryptonit-BOT",
    version="0.2.1",  # Ensure this follows Semantic Versioning
    description="A bot for encryption and decryption using Telegram",
    author="ruslanlap",
    author_email="your.email@example.com",
    url="https://github.com/ruslanlap/Cryptonit-BOT-COPYY",
    packages=find_packages(),
    install_requires=[
        "cryptography",
        "pyTelegramBotAPI",
    ],
    entry_points={
        'console_scripts': [
            'cryptonit-bot=your_package.cryptonit:main',  # Replace with actual module and function
        ],
    },
)
