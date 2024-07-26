import os
import telebot
from telebot import logging, types
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding, hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import uuid
import logging

# Замініть на свій токен бота
BOT_TOKEN = os.getenv('YOUR_BOT_TOKEN')

if BOT_TOKEN is None:
    raise ValueError("No bot token provided. Please set the YOUR_BOT_TOKEN environment variable.")

print(f"Bot token: {BOT_TOKEN}")  # Debug print

bot = telebot.TeleBot(BOT_TOKEN)

# Функція для генерації ключа з пароля
def generate_key(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

# Функція для шифрування
def encrypt(message, password):
    backend = default_backend()
    salt = os.urandom(16)
    key = generate_key(password, salt)
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(message.encode()) + padder.finalize()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    return base64.b64encode(salt + iv + ciphertext).decode('utf-8')

# Функція для дешифрування
def decrypt(encrypted_message, password):
    backend = default_backend()
    encrypted = base64.b64decode(encrypted_message.encode('utf-8'))
    salt = encrypted[:16]
    iv = encrypted[16:32]
    key = generate_key(password, salt)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    decryptor = cipher.decryptor()
    unpadder = padding.PKCS7(128).unpadder()
    plaintext_padded = decryptor.update(encrypted[32:]) + decryptor.finalize()
    plaintext = unpadder.update(plaintext_padded) + unpadder.finalize()
    return plaintext.decode('utf-8')

# Функція для екранування спеціальних символів у режимі MarkdownV2
def escape_markdown_v2(text):
    escape_chars = r"\_*[]()~`>#+-=|{}.!"
    return ''.join(['\\' + char if char in escape_chars else char for char in text])

# Створення клавіатури
def create_main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    encrypt_button = types.KeyboardButton("/encrypt🔒")
    decrypt_button = types.KeyboardButton("/decrypt🔓")
    help_button = types.KeyboardButton("/startℹ️")
    markup.add(encrypt_button, decrypt_button, help_button)
    return markup

# Обробник команди /start або HELP
@bot.message_handler(commands=['startℹ️','start', 'help'])
def send_welcome(message):
    response = f"👋 Вітаю, {message.from_user.first_name}! Я бот для шифрування/дешифрування. Використовуйте команди нижче або скорочення:\n\n" \
               "🔒 /encrypt або /e - Шифрувати повідомлення\n" \
               "🔓 /decrypt або /d - Дешифрувати повідомлення\n" \
               "ℹ️ /start або /help - Отримати допомогу\n\n" \
               "Не забудьте, що безпека вашого паролю дуже важлива! Ніколи не діліться своїм паролем з іншими людьми."
    bot.reply_to(message, response, reply_markup=create_main_menu())

# Обробник команди /encrypt
@bot.message_handler(commands=['encrypt🔒', 'e'])
def encrypt_command(message):
    bot.reply_to(message, "🔒 Будь ласка, введіть пароль для шифрування:")
    bot.register_next_step_handler(message, get_password_for_encryption)

def get_password_for_encryption(message):
    password = message.text
    bot.reply_to(message, "📧 Будь ласка, відправте повідомлення для шифрування:")
    bot.register_next_step_handler(message, lambda msg: encrypt_message(msg, password))

def encrypt_message(message, password):
    text = message.text
    encrypted = encrypt(text, password)
    escaped_encrypted = escape_markdown_v2(encrypted)
    bot.reply_to(message, f"🔐 Зашифроване повідомлення:\n{escaped_encrypted}", reply_markup=create_main_menu())

    # Save the encrypted message and password to a file
    file_path = "Crypt.txt"
    instructions_path = "Instructions.txt"
    save_encrypted_message(encrypted, password, file_path, instructions_path)

    # Send the file as a document
    with open(file_path, 'rb') as file:
        bot.send_document(message.chat.id, file, caption="🔐 Ваше зашифроване повідомлення", reply_markup=create_main_menu())

def save_encrypted_message(encrypted_message, password, file_path, instructions_path):
    try:
        with open(file_path, 'w') as file:
            file.write(f"Password: {password}\n\nEncrypted Message:\n{encrypted_message}\n\n")
            # Append instructions from Instructions.txt
            if os.path.exists(instructions_path):
                with open(instructions_path, 'r') as instructions_file:
                    file.write(instructions_file.read())
            else:
                logging.warning(f"Instructions file not found: {instructions_path}")
        logging.debug(f"Encrypted message and password saved to: {file_path}")
    except Exception as e:
        logging.error(f"Failed to save encrypted message and password: {e}")

# Обробник команди /decrypt
@bot.message_handler(commands=['decrypt🔓', 'd'])
def decrypt_command(message):
    bot.reply_to(message, "🔓 Будь ласка, введіть пароль для дешифрування:")
    bot.register_next_step_handler(message, get_password_for_decryption)

def get_password_for_decryption(message):
    password = message.text
    bot.reply_to(message, "📧 Будь ласка, відправте зашифроване повідомлення для дешифрування:")
    bot.register_next_step_handler(message, lambda msg: decrypt_message(msg, password))

def decrypt_message(message, password):
    encrypted_text = message.text
    try:
        decrypted = decrypt(encrypted_text, password)
        escaped_message = escape_markdown_v2(decrypted)
        bot.reply_to(message, f"🔓 Розшифроване повідомлення:\n||{escaped_message}||", parse_mode='MarkdownV2', reply_markup=create_main_menu())
    except Exception as e:
        escaped_error = escape_markdown_v2(str(e))
        bot.reply_to(message, f"⚠️ Помилка дешифрування: {escaped_error}. Переконайтеся, що повідомлення зашифроване правильно.", reply_markup=create_main_menu())

    # Save the decrypted message and password to a file
    file_path = "Decrypted.txt"
    save_decrypted_message(decrypted, password, file_path)

    # Send the file as a document
    with open(file_path, 'rb') as file:
        bot.send_document(message.chat.id, file, caption="🔓 Ваше розшифроване повідомлення", reply_markup=create_main_menu())

def save_decrypted_message(decrypted_message, password, file_path):
    try:
        with open(file_path, 'w') as file:
            file.write(f"Password: {password}\n\nDecrypted Message:\n{decrypted_message}")
        logging.debug(f"Decrypted message and password saved to: {file_path}")
    except Exception as e:
        logging.error(f"Failed to save decrypted message and password: {e}")

# Запуск бота
bot.polling()
