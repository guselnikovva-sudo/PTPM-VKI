import logging
import math


logging.basicConfig(
    level=logging.INFO,
)

logger = logging.getLogger(__name__)


def calculate_triangle(side_a: str, side_b: str, side_c: str):

    invalid_coordinates = [
        (-2, -2),
        (-2, -2),
        (-2, -2)
    ]

    try:
        a = float(side_a)
        b = float(side_b)
        c = float(side_c)

    except (ValueError, TypeError):
        logger.error("Получены нечисловые входные данные")
        return "", invalid_coordinates

    if not all(math.isfinite(x) and x > 0 for x in (a, b, c)):
        logger.error(
            "Стороны должны быть положительными конечными числами"
        )

        return "не треугольник", [
            (-1, -1),
            (-1, -1),
            (-1, -1)
        ]

    if a + b <= c or a + c <= b or b + c <= a:
        logger.error(
            "Из данных сторон невозможно построить треугольник"
        )

        return "не треугольник", [
            (-1, -1),
            (-1, -1),
            (-1, -1)
        ]

    if math.isclose(a, b) and math.isclose(b, c):
        triangle_type = "равносторонний"

    elif (
        math.isclose(a, b)
        or math.isclose(a, c)
        or math.isclose(b, c)
    ):
        triangle_type = "равнобедренный"

    else:
        triangle_type = "разносторонний"

    x = (a * a + b * b - c * c) / (2 * a)

    y_squared = b * b - x * x

    y = math.sqrt(max(0, y_squared))

    max_dimension = max(a, x, y)

    if max_dimension == 0:
        logger.error("Невозможно выполнить масштабирование")

        return "не треугольник", [
            (-1, -1),
            (-1, -1),
            (-1, -1)
        ]

    scale = 90 / max(a, x, y)

    x1 = 5
    y1 = 5

    x2 = 5 + a * scale
    y2 = 5

    x3 = 5 + x * scale
    y3 = 5 + y * scale

    coordinates = [
        (round(x1), round(y1)),
        (round(x2), round(y2)),
        (round(x3), round(y3))
    ]


    return triangle_type, coordinates


def main():

    print("=== Вычисление вида треугольника ===")

    side_a = input("Введите сторону A: ")
    side_b = input("Введите сторону B: ")
    side_c = input("Введите сторону C: ")

    triangle_type, coordinates = calculate_triangle(
        side_a,
        side_b,
        side_c
    )

    print()
    print("Тип треугольника:", triangle_type)
    print("Координаты вершин:", coordinates)


if __name__ == "__main__":
    main()