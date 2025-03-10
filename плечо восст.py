import numpy as np
import matplotlib.pyplot as plt

class StabilityCalculator:
    def __init__(self, length, width, draft, KG, angles):
        """
        Инициализация калькулятора остойчивости.

        Args:
            length (float): Длина судна по ватерлинии (в метрах).
            width (float): Ширина судна (в метрах).
            draft (float): Осадка судна (в метрах).
            KG (float): Высота центра тяжести от киля (в метрах).
            angles (list): Список углов крена для расчета (в градусах).
        """
        self.length = length
        self.width = width
        self.draft = draft
        self.KG = KG
        self.angles = np.radians(angles)  # Преобразуем углы в радианы
        self.g = 9.81  # Ускорение свободного падения (м/с^2)
        self.rho = 1025 # Плотность морской воды

    def calculate_righting_arm(self, angle):
        """
        Расчет восстанавливающего плеча (GZ) для заданного угла крена.

        Args:
            angle (float): Угол крена в радианах.

        Returns:
            float: Значение восстанавливающего плеча (GZ) в метрах.
        """
        # **ВНИМАНИЕ: Замените эту функцию на вашу реальную функцию для GZ**
        # Это очень упрощенный пример, предполагающий малые углы крена и простую форму корпуса.
        # Для реальных расчетов вам потребуется более сложная модель, учитывающая форму корпуса
        # при различных углах крена.  Это может включать в себя интерполяцию из таблиц или использование численных методов.

        # Пример: GZ = GM * sin(angle) + поправка на форму
        # Этот пример предполагает, что у вас есть оценка GM (метацентрической высоты)
        # Можно заменить приблизительным значением, например: GM = 0.1 * width (это ОЧЕНЬ грубое приближение!)
        GM = 0.01 * self.width # Очень грубое приближение
        GZ = GM * np.sin(angle)

        # Добавим поправку на форму (это просто пример, замените на что-то более разумное)
        GZ += 0.01 * np.sin(2 * angle)  # Пример поправки, дающей небольшой "горб" на кривой

        return GZ

    def calculate_stability_data(self):
        """
        Расчет значений восстанавливающего плеча для всех углов крена.

        Returns:
            tuple: Списки углов (в градусах) и соответствующих значений GZ.
        """
        gz_values = [self.calculate_righting_arm(angle) for angle in self.angles]
        angles_degrees = np.degrees(self.angles)
        return angles_degrees, gz_values

    def plot_stability_curve(self, angles, gz_values):
        """
        Построение кривой статической остойчивости (GZ кривая).

        Args:
            angles (list): Список углов крена в градусах.
            gz_values (list): Список значений восстанавливающего плеча (GZ) в метрах.
        """
        plt.plot(angles, gz_values)
        plt.xlabel("Угол крена (градусы)")
        plt.ylabel("Восстанавливающее плечо GZ (метры)")
        plt.title("Кривая статической остойчивости")
        plt.grid(True)
        plt.show()

    def evaluate_stability_criteria(self, angles, gz_values):
        """
        Оценка соответствия критериям остойчивости (пример).

        Args:
            angles (list): Список углов крена в градусах.
            gz_values (list): Список значений восстанавливающего плеча (GZ) в метрах.

        Returns:
            dict: Результаты оценки критериев.
        """
        # **ВНИМАНИЕ: Замените эти критерии на ваши собственные.**
        # Это примеры критериев, основанные на IMO A.749(18) (небольшие суда).
        # Конкретные критерии зависят от типа судна и нормативных требований.
        results = {}

        # Критерий 1: Максимальное значение GZ должно быть не менее 0.2 м
        max_gz = max(gz_values)
        results['Максимальное_GZ'] = max_gz
        results['Максимальное_GZ_OK'] = max_gz >= 0.2

        # Критерий 2: Угол при максимальном GZ должен быть не менее 25 градусов
        angle_at_max_gz = angles[gz_values.index(max_gz)]
        results['Угол_при_максимальном_GZ'] = angle_at_max_gz
        results['Угол_при_максимальном_GZ_OK'] = angle_at_max_gz >= 25

        # Критерий 3: Площадь под кривой GZ до 30 градусов должна быть не менее 0.055 м.рад
        # (Приближенно рассчитываем как сумму площадей прямоугольников)
        area_to_30 = np.trapz(gz_values[:len([a for a in angles if a <= 30])], x=np.radians(angles[:len([a for a in angles if a <= 30])]))
        results['Площадь_под_кривой_до_30_градусов'] = area_to_30
        results['Площадь_под_кривой_до_30_градусов_OK'] = area_to_30 >= 0.055

        return results

# --- Пример использования ---
if __name__ == "__main__":
    # **ВНИМАНИЕ: Замените эти значения на данные вашего катера**
    length = 1.198 # метры
    width = 0.3415   # метры
    draft = 0.4   # метры
    KG = 0.71    # метры
    angles = np.arange(0, 91, 5)  # Углы крена от 0 до 90 градусов с шагом 5

    calculator = StabilityCalculator(length, width, draft, KG, angles)
    angles_degrees, gz_values = calculator.calculate_stability_data()
    calculator.plot_stability_curve(angles_degrees, gz_values)

    # Оцениваем критерии остойчивости
    criteria_results = calculator.evaluate_stability_criteria(angles_degrees, gz_values)
    print("\nОценка критериев остойчивости:")
    for key, value in criteria_results.items():
        print(f"{key}: {value}") 
