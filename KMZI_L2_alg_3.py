# Алгоритм 2.3 "Бесключевое дешифрование сообщения в случае малого порядка элемента e"

def string_to_int(message):
    """Преобразование строки в целое число"""
    return int.from_bytes(message.encode('utf-8'), 'big')


def int_to_string(number):
    """Преобразование целого числа в строку"""
    return number.to_bytes((number.bit_length() + 7) // 8, 'big').decode('utf-8')


def keyless_decryption(n, c, e):
    c_i = c  # c_0 = c
    i = 1

    while True:
        try:
            # Вычисляем c_i ≡ c_{i-1}^e ≡ c_0^{e^i} mod n
            c_i = pow(c_i, e, n)

            # Проверяем c_i ≡ c mod n
            if c_i == c:
                # Нашли решение, возвращаем предыдущее значение
                print(i-1)
                return pow(c, e ** (i - 1), n)

            i += 1

            if i > 1000:
                print("\nПревышено максимальное количество итераций (1000).")
                return None

        except Exception as ex:
            print(f"\nОшибка при дешифровании: {ex}")
            return None


def main():
    try:
        # Ввод параметров
        n = int(input("Введите модуль n: "))
        e = int(input("Введите открытую экспоненту e: "))
        m_str = input("Введите сообщение m: ")

        # Преобразование сообщения в число и шифрование
        m = string_to_int(m_str)
        if m >= n:
            print("Ошибка: сообщение слишком большое для данного n")
            return
        c = pow(m, e, n)
        print(f"\nЗашифрованное сообщение c: {c}")

        # Запрос секретного ключа для проверки
        check = input("Проверить результат с помощью секретного ключа d? (y/n): ").lower()
        d = None
        if check == 'y':
            d = int(input("Введите секретный ключ d: "))

        # Атака бесключевого дешифрования
        m_attack = keyless_decryption(n, c, e)

        if m_attack is not None:
            m_str_attack = int_to_string(m_attack)
            print(f"\nРезультат бесключевого дешифрования (число): {m_attack}")
            print(f"Результат бесключевого дешифрования (строка): '{m_str_attack}'")

            # Проверка с помощью секретного ключа
            if d is not None:
                m_check = pow(c, d, n)
                m_str_check = int_to_string(m_check)
                print(f"\nРезультат обычного дешифрования (число): {m_check}")
                print(f"Результат обычного дешифрования (строка): '{m_str_check}'")

                if m_attack == m_check:
                    print("\nРезультаты совпадают! Атака выполнена успешно.")
                else:
                    print("\nРезультаты не совпадают! Возможна ошибка в параметрах.")
        else:
            print("\nАтака не удалась.")

    except ValueError:
        print("\nОшибка: все числовые параметры должны быть целыми числами.")
    except Exception as ex:
        print(f"\nНеожиданная ошибка: {ex}")


if __name__ == "__main__":
    main()

# n = 143
# e = 67
# c = 47
# d = 43
# a = 5

# n = 45571
# e = 34937
# d = 32561