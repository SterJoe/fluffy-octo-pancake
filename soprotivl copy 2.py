import math
import matplotlib.pyplot as plt
import numpy as np

def calculate_resistance(Lwl, B, T, V_range, Aw=None, rho=1025, nu=1.188e-6):
    """
    Оценивает буксировочное сопротивление катамарана и оценивает Cwp и Cb, если они не заданы.
    Водоизмещение Delta (в кг) рассчитывается на основе Volume и rho.
    Volume оценивается по упрощенной формуле.

    Args:
        Lwl: Длина по ватерлинии (м).
        B: Ширина корпуса одного поплавка (м).
        T: Осадка (м).
        V_range: Диапазон скоростей (список или numpy array) в м/с.
        Aw: Площадь ватерлинии (м^2). Если None, будет оценена.
        rho: Плотность воды (кг/м^3).
        nu: Кинематическая вязкость воды (м^2/с).

    Returns:
        Rt_values: Список полных сопротивлений (Н).
        Rv_values: Список вязкостных сопротивлений (Н).
        Rr_values: Список остаточных сопротивлений (Н).
        Cwp: Коэффициент полноты площади ватерлинии (оценка).
        Cb: Коэффициент общей полноты (оценка).
        Delta: Водоизмещение (кг).
        Volume: Оцененный объем (м^3)
    """

    # 1. Оценка объема водоизмещения
    # Простая оценка: предполагаем форму параллелепипеда
    Volume = Lwl * B * T * 2  # Умножаем на 2, так как два поплавка
    print("Объем водоизмещения оценен. Требуется более точное значение.")

    # 2. Расчет водоизмещения (Delta) в кг
    Delta = rho * Volume
    print(f"Водоизмещение (Delta): {Delta:.2f} кг")

    # 3. Расчет площади ватерлинии (если не задана)
    if Aw is None:
        # Простая оценка: предполагаем эллиптическую форму ватерлинии каждого поплавка
        # Это очень приблизительно!  Для более точной оценки требуется знание формы корпуса.
        Aw = 0.7 * Lwl * B * 2  # Умножаем на 2, так как два поплавка. 0.7 - примерный коэффициент
        print("Площадь ватерлинии оценена. Требуется более точное значение.")

    # 4. Расчет коэффициентов полноты (если не заданы)
    Cb = Volume / (Lwl * B * T * 2)  # Умножаем на 2, так как два поплавка.
    Cwp = Aw / (Lwl * B * 2)  # Умножаем на 2, так как два поплавка.

    print(f"Оцененный коэффициент общей полноты (Cb): {Cb:.2f}")
    print(f"Оцененный коэффициент полноты площади ватерлинии (Cwp): {Cwp:.2f}")

    # 5. Расчет смоченной поверхности (S)
    #   Приближенная формула (нужно адаптировать для конкретной формы)
    S = 2.0 * (2.0 * Lwl * T + B * Lwl)  # Умножаем на 2, так как два корпуса

    # Списки для хранения результатов
    Rt_values = []
    Rv_values = []
    Rr_values = []
    for V in V_range:
        # 6. Расчет числа Рейнольдса (Re)
        Re = (V * Lwl) / nu

        # 7. Расчет коэффициента вязкостного сопротивления (Cf)
        if Re > 100:
            Cf = 0.075 / (math.log10(Re) - 2)**2
        else:
            Cf = 0.0  # Или другое разумное значение

        # 8. Расчет остаточного сопротивления (Rr)
        #   Используем приближенную формулу, зависящую от числа Фруда и коэффициентов формы.
        #   Эта формула очень упрощена и может давать большие погрешности.
        Fn = V / math.sqrt(9.81 * Lwl)  # Число Фруда
        # Предположим, что остаточное сопротивление составляет примерно 10-20% от вязкостного
        Cr = 0.15 * Cf  # Приближенное значение. Требуются экспериментальные данные

        # 9. Расчет полного сопротивления (Rt)
        Rv = 0.5 * rho * V**2 * S * Cf  # Вязкостное сопротивление
        Rr = 0.5 * rho * V**2 * S * Cr  # Остаточное сопротивление
        Rt = Rv + Rr

        Rt_values.append(Rt)
        Rv_values.append(Rv)
        Rr_values.append(Rr)

    # Вывод графиков
    plt.figure(figsize=(10, 6))
    plt.plot(V_range, Rt_values, label="Полное сопротивление (Rt)")
    plt.plot(V_range, Rv_values, label="Вязкостное сопротивление (Rv)")
    plt.plot(V_range, Rr_values, label="Волновое сопротивление (Rr)")
    plt.xlabel("Скорость (м/с)")
    plt.ylabel("Сопротивление (Н)")
    plt.title("Зависимость сопротивления от скорости")
    plt.grid(True)
    plt.legend()
    plt.show()

    return Rt_values, Rv_values, Rr_values, Cwp, Cb, Delta, Volume


# Пример использования:
Lwl = 5.0  # м
B = 0.5  # м
T = 0.3  # м
V_range = np.arange(0, 25, 0.1)  # Диапазон скоростей от 0 до 10 м/с с шагом 0.1 м/с

Rt_values, Rv_values, Rr_values, Cwp, Cb, Delta, Volume = calculate_resistance(Lwl, B, T, V_range)