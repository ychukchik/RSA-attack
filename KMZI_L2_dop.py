from functools import reduce
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import unpad


def chinese_remainder_theorem(n, a):
    """Реализация китайской теоремы об остатках"""
    sum = 0
    prod = reduce(lambda a, b: a * b, n)  # 1. Вычисляем произведение всех n_i
    for n_i, a_i in zip(n, a):
        p = prod // n_i                   # 2. Для каждого n_i: p = произведение всех остальных
        sum += a_i * pow(p, -1, n_i) * p  # 3. Добавляем a_i в общее решение
    return sum % prod                     # 4. Возвращаем результат по модулю prod


def find_integer_root(x, e):
    """Нахождение целочисленного корня степени e с использованием бинарного поиска"""
    low = 0 # минимально возможный корень
    high = x # максимальный
    while low <= high:
        mid = (low + high) // 2 # середина текущего диапазона
        power = mid ** e
        if power == x:   # нашли корень
            return mid
        elif power < x:  # корень слева
            low = mid + 1
        else:            # корень справа
            high = mid - 1
    # Если точный корень не найден, попробуем ближайшие значения вокруг примерного корня
    for delta in [-1, 1, -2, 2, -3, 3]:
        candidate = int(round(x ** (1/e)) + delta)
        if candidate >= 0 and candidate ** e == x:
            return candidate
    return None


def decrypt_aes(ciphertext, key, iv, original_length):
    """Расшифровка AES-256 в режиме CBC"""
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = cipher.decrypt(ciphertext)
    # Удаляем padding
    try:
        decrypted = unpad(decrypted, AES.block_size)
    except ValueError:
        # Если padding некорректный, просто обрезаем по original_length
        pass
    return decrypted[:original_length]


def read_keys_and_ciphertexts(filename):
    """Чтение ключей и шифртекстов из файла"""
    with open(filename, 'r') as f:
        lines = f.readlines()

    keys = []
    ciphertexts = []
    original_length = None
    iv = None

    for line in lines:
        if line.startswith('n='):
            n = int(line.split('=')[1].strip())
        elif line.startswith('e='):
            e = int(line.split('=')[1].strip())
            keys.append((e, n))
        elif line.startswith('c='):
            c = int(line.split('=')[1].strip())
            ciphertexts.append(c)
        elif line.startswith('Original length:'):
            original_length = int(line.split(':')[1].strip())
        elif line.startswith('IV:'):
            iv_hex = line.split(':')[1].strip()
            iv = bytes.fromhex(iv_hex)

    return keys, ciphertexts, original_length, iv


def main():
    # Запрашиваем имя файла с параметрами
    input_file = input("Введите имя файла с параметрами (params.txt): ")

    try:
        # 1. Чтение входных данных
        keys, ciphertexts, original_length, iv = read_keys_and_ciphertexts(input_file)

        if not keys or not ciphertexts:
            print("Ошибка: не найдены ключи или шифртексты в файле")
            return

        # Проверка, что все e одинаковы (малый общий показатель)
        e = keys[0][0]
        for (e_i, n_i) in keys[1:]:
            if e_i != e:
                print("Ошибка: показатели e не одинаковы")
                return

        # 2. Восстановление m^e по КТО
        moduli = [n for (e_i, n) in keys]
        remainders = ciphertexts
        m_e = chinese_remainder_theorem(moduli, remainders)

        # 3. Извлечение корня степени e
        m = find_integer_root(m_e, e)
        if m is None:
            print(f"Не удалось найти целочисленный корень степени {e} из {m_e}")
            return

        # 4. Преобразование m в байты (это AES ключ)
        try:
            key = m.to_bytes(32, byteorder='big')  # AES-256 требует 32 байта
        except OverflowError:
            print(f"Ошибка: m={m} слишком большое для преобразования в 32 байта")
            return

        # 5. Чтение зашифрованного файла
        ciphertext_file = input("Введите имя файла с AES-шифртекстом (AES_enc.txt): ")
        if not ciphertext_file:
            ciphertext_file = input_file.replace('.txt', '.enc')

        with open(ciphertext_file, 'rb') as f:
            ciphertext = f.read()

        # 6. Расшифровка AES
        plaintext = decrypt_aes(ciphertext, key, iv, original_length)

        # 7. Сохранение результата
        output_file = input("Введите имя файла для сохранения результата (result.txt): ")
        if not output_file:
            output_file = input_file.replace('.txt', '.decrypted')

        with open(output_file, 'wb') as f:
            f.write(plaintext)

        print(f"Сообщение успешно расшифровано и сохранено в {output_file}")

    except FileNotFoundError:
        print(f"Ошибка: файл {input_file} не найден")
    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")


if __name__ == "__main__":
    main()