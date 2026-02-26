# Алгоритм 2.1 "Разложение составного числа на множители по
# известным показателям RSA"

import random
import math

def factorize_n(n, eB, dB, eA, max_attempts=100):
    # Шаг 1: Представить разность eB * dB - 1 в виде 2^f * s
    difference = eB * dB - 1
    f = 0
    while difference % 2 == 0:
        difference //= 2
        f += 1
    s = difference

    attempts = 0
    while attempts < max_attempts:
        attempts += 1
        # Шаг 2: Выбрать случайное a и вычислить b = a^s mod n
        a = random.randint(2, n - 1)
        b = pow(a, s, n)

        # Шаг 3: Найти l такое, что b^(2^l) ≡ 1 mod n
        for l in range(f):
            prev_b = b
            b = pow(b, 2, n)
            if b == 1:
                if prev_b != n - 1:
                    t = prev_b
                    # Шаг 4: Найти p и q
                    p = math.gcd(t + 1, n)
                    q = math.gcd(t - 1, n)
                    # Проверка, что p и q корректны
                    if p > 1 and q > 1:
                        # Шаг 5: Вычислить phi(n) и dA
                        phi_n = (p - 1) * (q - 1)
                        if phi_n == 0:
                            print("Ошибка: phi(n) равно 0. Повторная попытка...")
                            break
                        if math.gcd(eA, phi_n) != 1:
                            print(f"Ошибка: eA = {eA} и phi(n) = {phi_n} не взаимно просты!")
                            return None
                        dA = pow(eA, -1, phi_n)
                        return (p, q), dA
                    else:
                        print("Ошибка: p или q равны 1. Повторная попытка...")
                        break
                break
        else:
            continue


    print(f"Не удалось найти делители после {max_attempts} попыток.")
    return None

def read_values_from_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        n = int(lines[0].strip())
        eB = int(lines[1].strip())
        dB = int(lines[2].strip())
        eA = int(lines[3].strip())
    return n, eB, dB, eA

# Путь к файлу
filename = input("Введите имя файла: ")
n, eB, dB, eA = read_values_from_file(filename)

result = factorize_n(n, eB, dB, eA)
if result:
    (p, q), dA = result
    print(f"p = {p}, \nq = {q},\ndA = {dA}")

    # Проверка корректности результатов
    if p * q == n:
        print("Успех: p и q являются делителями n.")
    else:
        print("Ошибка: p и q не являются делителями n.")

    phi_n = (p - 1) * (q - 1)
    if (eA * dA) % phi_n == 1:
        print("Успех: dA является корректным закрытым ключом.")
    else:
        print("Ошибка: dA не является корректным закрытым ключом.")
else:
    print("Алгоритм не смог найти делители.")