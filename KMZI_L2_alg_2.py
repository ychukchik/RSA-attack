# Алгоритм 2.2 "Атака Винера на криптосистему RSA"

import math


def wiener_attack(n, e):

    # Шаг 1: Разложение e/n в непрерывную дробь
    def continued_fraction(e, n):
        cf = []
        while n != 0:
            cf.append(e // n)
            e, n = n, e % n
        return cf

    # Шаг 2: Вычисление подходящих дробей
    def convergents(cf):
        convergents = []
        for i in range(len(cf)):
            if i == 0:
                num = cf[i]
                den = 1
            elif i == 1:
                num = cf[i] * cf[i - 1] + 1
                den = cf[i]
            else:
                num = cf[i] * convergents[i - 1][0] + convergents[i - 2][0]
                den = cf[i] * convergents[i - 1][1] + convergents[i - 2][1]
            convergents.append((num, den))
        return convergents

    cf = continued_fraction(e, n)
    convergents = convergents(cf)

    # Шаг 2.2: Проверка каждой подходящей дроби
    for (k, d) in convergents:
        # Пропускаем случаи, когда d=0
        if d == 0:
            continue

        # Проверяем, является ли k/d подходящей дробью для e/n
        if k == 0:
            continue

        # Проверяем условие атаки Винера
        phi = (e * d - 1) // k

        # Решаем квадратное уравнение x^2 - (n - phi + 1)x + n = 0
        a = 1
        b = -(n - phi + 1)
        c = n

        # Вычисляем дискриминант
        discriminant = b * b - 4 * a * c
        if discriminant < 0:
            continue

        # Проверяем, является ли дискриминант квадратом целого числа
        sqrt_discriminant = math.isqrt(discriminant)
        if sqrt_discriminant * sqrt_discriminant != discriminant:
            continue

        # Проверяем, что корни целые
        if (-b + sqrt_discriminant) % (2 * a) != 0 or (-b - sqrt_discriminant) % (2 * a) != 0:
            continue

        # Если все проверки пройдены, возвращаем d
        return d

    # Если ничего не найдено
    return None


def get_user_input():

    while True:
        try:
            n = int(input("Введите модуль n: "))
            e = int(input("Введите открытую экспоненту e: "))

            if n <= 0 or e <= 0:
                print("Ошибка: n и e должны быть положительными числами.")
                continue

            return n, e
        except ValueError:
            print("Ошибка: введите целые числа для n и e.")


def main():
    n, e = get_user_input()

    d = wiener_attack(n, e)

    if d is not None:
        print(f"Успех! Найден закрытый ключ d: {d}")

        # Проверка
        try:
            m = 12345
            c = pow(m, e, n)
            m_decrypted = pow(c, d, n)
            print(f"\nПроверка: {m}^e mod n = {c}")
            print(f"{c}^d mod n = {m_decrypted}")
            print(f"Исходное сообщение и расшифрованное совпадают? {m == m_decrypted}")
        except ValueError:
            print("Проверка не пройдена.")
    else:
        print("\nАтака не удалась.")


if __name__ == "__main__":
    main()

# n = 1220275921
# e = 1073780833