import random
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
from Cryptodome.Util.Padding import pad, unpad
from sympy import isprime


def generate_prime(bits):
    """Генерация простого числа заданной длины"""
    while True:
        p = random.getrandbits(bits)
        if p % 2 == 0:
            p += 1
        if isprime(p):
            return p


def generate_rsa_keys(e, bits=512):
    """Генерация пары RSA ключей с заданным e"""
    while True:
        p = generate_prime(bits // 2)
        q = generate_prime(bits // 2)
        if p != q:
            n = p * q
            phi = (p - 1) * (q - 1)
            if gcd(e, phi) == 1:
                return (e, n)


def gcd(a, b):
    """Наибольший общий делитель"""
    while b:
        a, b = b, a % b
    return a


def generate_test_parameters(num_users=3, e=3, message=None):
    """Генерация тестовых параметров"""
    # Генерируем случайное сообщение (AES ключ)
    m = random.getrandbits(256)
    key = m.to_bytes(32, byteorder='big')

    # Генерируем случайный IV для AES
    iv = get_random_bytes(16)

    # Используем предоставленное сообщение или генерируем случайное
    if message is None:
        original_message = get_random_bytes(64)
    else:
        original_message = message.encode('utf-8') if isinstance(message, str) else message

    original_length = len(original_message)

    # Шифруем сообщение AES-256-CBC
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(original_message, AES.block_size))

    # Проверяем, что можем расшифровать
    try:
        cipher_dec = AES.new(key, AES.MODE_CBC, iv)
        decrypted = unpad(cipher_dec.decrypt(ciphertext), AES.block_size)
        if decrypted != original_message:
            raise ValueError("Decryption test failed")
    except Exception as e:
        raise ValueError(f"Decryption test failed: {str(e)}")

    # Генерируем RSA ключи для пользователей
    keys = [generate_rsa_keys(e) for _ in range(num_users)]

    # Шифруем m с использованием каждого ключа
    ciphertexts = [pow(m, e, n) for (e, n) in keys]

    return {
        'keys': keys,
        'ciphertexts': ciphertexts,
        'original_length': original_length,
        'iv': iv,
        'aes_ciphertext': ciphertext,
        'original_message': original_message,
        'aes_key': key
    }


def save_parameters_to_file(parameters, filename):
    """Сохранение параметров в файл"""
    base_filename = filename.replace('.txt', '')

    # Сохраняем параметры RSA и AES
    with open(filename, 'w') as f:
        # Записываем ключи и шифртексты
        for i, ((e, n), c) in enumerate(zip(parameters['keys'], parameters['ciphertexts'])):
            f.write(f"n={n}\n")
            f.write(f"e={e}\n")
            f.write(f"c={c}\n")

        # Записываем дополнительные параметры
        f.write(f"Original length: {parameters['original_length']}\n")
        f.write(f"IV: {parameters['iv'].hex()}\n")

    # Сохраняем зашифрованное AES сообщение
    ciphertext_file = f"AES_enc.txt"
    with open(ciphertext_file, 'wb') as f:
        f.write(parameters['aes_ciphertext'])

    # Сохраняем оригинальное сообщение
    original_file = f"{base_filename}_original.txt"
    with open(original_file, 'wb') as f:
        f.write(parameters['original_message'])

    # Сохраняем параметры для проверки
    check_file = f"{base_filename}_check.txt"
    with open(check_file, 'w') as f:
        f.write(f"AES key (hex): {parameters['aes_key'].hex()}\n")
        f.write(f"AES key (int): {int.from_bytes(parameters['aes_key'], 'big')}\n")
        f.write(f"Original message length: {parameters['original_length']}\n")
        f.write(f"IV (hex): {parameters['iv'].hex()}\n")

    return ciphertext_file, original_file, check_file


def main():
    print("Генератор параметров для бесключевого дешифрования")

    # Запрашиваем имя файла для сохранения
    filename = input("Введите имя файла для сохранения параметров (например: params.txt): ").strip()
    if not filename.endswith('.txt'):
        filename += '.txt'

    # Параметры генерации
    num_users = int(input("Введите количество пользователей (по умолчанию 3): ") or "3")
    e = int(input("Введите значение e (по умолчанию 3): ") or "3")

    # Запрос сообщения для шифрования
    message = input("Введите сообщение для шифрования: ").strip()
    if not message:
        message = None
        print("Будет использовано случайное сообщение")

    # Генерируем параметры
    print("\nГенерация параметров...")
    try:
        params = generate_test_parameters(num_users, e, message)
    except ValueError as ve:
        print(f"Ошибка при генерации параметров: {ve}")
        return

    # Сохраняем в файл
    cipher_file, original_file, check_file = save_parameters_to_file(params, filename)

    print(f"\nПараметры успешно сохранены:")
    print(f"- Основные параметры: {filename}")
    print(f"- Зашифрованное сообщение: {cipher_file}")
    print(f"- Оригинальное сообщение: {original_file}")

    # Выводим информацию для проверки
    print("\nСгенерированные параметры:")
    print(f"- Количество пользователей: {num_users}")
    print(f"- Общий показатель e: {e}")
    print(f"- Длина сообщения: {params['original_length']} байт")
    print(f"- IV: {params['iv'].hex()}")

    if message:
        print(f"- Исходное сообщение: {message}")
    else:
        print(f"- Случайное сообщение (hex): {params['original_message'].hex()}")

    print(f"- Ключ AES (int): {int.from_bytes(params['aes_key'], 'big')}")


if __name__ == "__main__":
    main()