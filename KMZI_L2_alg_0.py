# Генерация параметров для Алгоритма 2.1 "Разложение составного числа на множители по
# известным показателям RSA"

import random
from math import gcd
from sympy import isprime, mod_inverse


# Генерация простого числа
def generate_prime(bits):
    while True:
        num = random.getrandbits(bits)
        num |= (1 << bits - 1) | 1  # Число нечетное и имеет заданную длину
        if isprime(num):
            return num


# Генерация параметров для RSA
def generate_rsa_parameters(bits=1024):
    while True:
        p = generate_prime(bits)
        q = generate_prime(bits)

        n = p * q
        phi_n = (p - 1) * (q - 1)

        while True:
            e = random.randint(2, phi_n - 1)
            if gcd(e, phi_n) == 1:
                break

        d = mod_inverse(e, phi_n)
        print(f"n = {n}")
        print(f"e = {e}")
        print(f"d = {d}")
        return p, q, n, e, d


# Генерация значений n, eB, dB, eA
def generate_values(bits=1024):
    # Генерация параметров для пользователя B
    p, q, n, eB, dB = generate_rsa_parameters(bits)
    # Генерация открытого ключа для пользователя A
    phi_n = (p - 1) * (q - 1)
    while True:
        eA = random.randint(2, phi_n - 1)
        if gcd(eA, phi_n) == 1:
            break

    return n, eB, dB, eA


# Сохранение значений в файл
def save_values_to_file(filename, n, eB, dB, eA):
    with open(filename, 'w') as file:
        file.write(f"{n}\n{eB}\n{dB}\n{eA}\n")


def main():
    bits = int(input("Введите количество бит для генерации простых чисел (например, 1024): "))
    filename = input("Введите имя файла для сохранения значений: ")

    n, eB, dB, eA = generate_values(bits)
    save_values_to_file(filename, n, eB, dB, eA)

    print(f"Значения сохранены в файл {filename}:")
    print(f"n = {n}")
    print(f"eB = {eB}")
    print(f"dB = {dB}")
    print(f"eA = {eA}")


if __name__ == "__main__":
    main()