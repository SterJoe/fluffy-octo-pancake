import numpy as np
from stl import mesh

def calculate_center_of_mass_single_material(stl_file):
    """
    Рассчитывает центр тяжести цельной STL-модели из одного материала и выводит продольное и вертикальное положение.

    Args:
        stl_file: Путь к STL-файлу.

    Returns:
        center_of_mass: Координаты центра тяжести (x, y, z).
    """

    try:
        # Загрузка STL-модели
        model = mesh.Mesh.from_file(stl_file)

        # Получение вершин треугольников
        vertices = model.vectors.reshape(-1, 3)

        # Расчет центра тяжести как среднего арифметического координат всех вершин
        center_of_mass = np.mean(vertices, axis=0)

        # Расчет продольного и вертикального положения (относительно начала координат)
        LCG = center_of_mass[0]  # X-координата
        VCG = center_of_mass[2]  # Z-координата

        return center_of_mass, LCG, VCG

    except FileNotFoundError:
        print(f"Ошибка: Файл '{stl_file}' не найден.")
        return None, None, None
    except Exception as e:
        print(f"Ошибка при обработке STL-файла: {e}")
        return None, None, None

# Пример использования:
stl_file = "katamaran.stl"  # Замените на путь к вашему STL-файлу
center_of_mass, LCG, VCG = calculate_center_of_mass_single_material(stl_file)

if center_of_mass is not None:
    print(f"Центр тяжести: {center_of_mass}")
    print(f"Продольное положение (LCG): {LCG:.3f}")
    print(f"Вертикальное положение (VCG): {VCG:.3f}")