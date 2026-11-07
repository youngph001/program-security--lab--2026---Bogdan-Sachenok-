import hashlib
import os

# --- ІМІТАЦІЯ БАЗИ ДАНИХ ---
users_db = {}

def register_user(username, password):
    """Реєстрація нового користувача з хешуванням пароля."""
    if username in users_db:
        return "Помилка: Користувач вже існує."
    
    # Генеруємо випадкову сіль
    salt = os.urandom(16)
    # Хешуємо пароль (використовуємо PBKDF2 з SHA-256)
    pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    
    # Зберігаємо в "базі" тільки хеш та сіль (сам пароль не зберігаємо)
    users_db[username] = {
        'salt': salt,
        'hash': pwd_hash
    }
    return f"Користувач {username} успішно зареєстрований."

def login_user(username, password):
    """Перевірка пароля під час входу."""
    user = users_db.get(username)
    if not user:
        # Загальне повідомлення, щоб не розкривати, чи існує логін
        return "Неправильний логін або пароль." 
    
    # Беремо сіль і хешуємо введений пароль
    salt = user['salt']
    new_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    
    # Порівнюємо хеші
    if new_hash == user['hash']:
        return f"Вхід успішний! Вітаємо, {username}."
    else:
        return "Неправильний логін або пароль."
