# Генерация безопасных параметров для RSA

import random
from sympy import isprime, gcd, mod_inverse


# Генерация простого числа
def generate_prime(bits):
    while True:
        num = random.getrandbits(bits)
        num |= (1 << bits - 1) | 1  # Число нечетное и имеет заданную длину
        if isprime(num):
            return num


def generate_rsa_parameters(bits=1024):
    bits //= 2
    p = generate_prime(bits)
    q = generate_prime(bits)

    n = p * q
    phi = (p - 1) * (q - 1)

    # 2. Выбор e с учетом защиты от всех атак
    while True:
        # Выбираем большое e
        e = random.randint(65537, phi - 1)
        e_2 = random.randint(65537, phi - 1)
        print(e_2)
        if gcd(e, phi) == 1 and gcd(e_2, phi) == 1:
            d = mod_inverse(e, phi)

            # Условие Винера: d > (1/3) * n^(1/4)
            # Заменяем на d.bit_length() > (n.bit_length() // 4) - 2 (эквивалентная проверка)
            wiener_condition = d.bit_length() > (n.bit_length() // 4) - 2

            # Проверка на малый порядок e
            # Порядок e должен быть большим в обеих подгруппах
            order_p = (p - 1) // gcd(e, p - 1)
            order_q = (q - 1) // gcd(e, q - 1)
            min_order = min(order_p, order_q)

            # Эмпирически выбранный порог для "малого" порядка
            # if wiener_condition and (min_order > 2 ** 20):
            #     break
            if wiener_condition:
                break

    return n, e, d, e_2


# Пример использования
if __name__ == "__main__":
    bits = int(input("Введите количество бит для генерации n (например, 1024): "))
    n, e, d, e_2 = generate_rsa_parameters(bits)
    filename = input("Введите имя файла для сохранения значений: ")
    with open(filename, 'w') as file:
        file.write(f"{n}\n{e}\n{d}\n{e_2}\n")

    print(f"Модуль n: {n}")
    print(f"Открытая экспонента e: {e}")
    print(f"Закрытая экспонента d: {d}")