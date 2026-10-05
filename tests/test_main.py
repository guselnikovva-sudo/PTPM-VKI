import unittest

from main import calculate_triangle


class TestCalculateTriangle(unittest.TestCase):

    def test_calculate_triangle_3_4_5(self):
        result = calculate_triangle("3", "4", "5")

        self.assertEqual(result[0], "разносторонний")

    def test_calculate_triangle_with_text_instead_of_number(self):
        result = calculate_triangle("abc", "4", "5")

        self.assertEqual(result[0], "")
        self.assertEqual(
            result[1],
            [(-2, -2), (-2, -2), (-2, -2)]
        )
    def test_calculate_triangle_with_empty_string(self):
        result = calculate_triangle("", "4", "5")

        self.assertEqual(result[0], "")
        self.assertEqual(
            result[1],
            [(-2, -2), (-2, -2), (-2, -2)]
        )

    def test_calculate_triangle_with_none(self):
        result = calculate_triangle(None, "4", "5")

        self.assertEqual(result[0], "")
        self.assertEqual(
            result[1],
            [(-2, -2), (-2, -2), (-2, -2)]
        )

    def test_calculate_triangle_with_negative_side(self):
        result = calculate_triangle("-3", "4", "5")

        self.assertEqual(result[0], "не треугольник")
        self.assertEqual(
            result[1],
            [(-1, -1), (-1, -1), (-1, -1)]
        )

    def test_calculate_triangle_with_zero_side(self):
        result = calculate_triangle("0", "4", "5")

        self.assertEqual(result[0], "не треугольник")
        self.assertEqual(
            result[1],
            [(-1, -1), (-1, -1), (-1, -1)]
        )

    def test_calculate_triangle_with_infinity(self):
        result = calculate_triangle("inf", "4", "5")

        self.assertEqual(result[0], "не треугольник")
        self.assertEqual(
            result[1],
            [(-1, -1), (-1, -1), (-1, -1)]
        )

    def test_calculate_triangle_with_nan(self):
        result = calculate_triangle("nan", "4", "5")

        self.assertEqual(result[0], "не треугольник")
        self.assertEqual(
            result[1],
            [(-1, -1), (-1, -1), (-1, -1)]
        )
    def test_triangle_does_not_exist_when_a_plus_b_equals_c(self):
        result = calculate_triangle("1", "2", "3")

        self.assertEqual(result[0], "не треугольник")
        self.assertEqual(
            result[1],
            [(-1, -1), (-1, -1), (-1, -1)]
        )

    def test_triangle_does_not_exist_when_a_plus_b_less_than_c(self):
        result = calculate_triangle("1", "2", "4")

        self.assertEqual(result[0], "не треугольник")
        self.assertEqual(
            result[1],
            [(-1, -1), (-1, -1), (-1, -1)]
        )

    def test_triangle_does_not_exist_when_a_plus_c_equals_b(self):
        result = calculate_triangle("1", "3", "2")

        self.assertEqual(result[0], "не треугольник")
        self.assertEqual(
            result[1],
            [(-1, -1), (-1, -1), (-1, -1)]
        )

    def test_triangle_does_not_exist_when_b_plus_c_equals_a(self):
        result = calculate_triangle("3", "1", "2")

        self.assertEqual(result[0], "не треугольник")
        self.assertEqual(
            result[1],
            [(-1, -1), (-1, -1), (-1, -1)]
        )
    def test_triangle_is_equilateral_when_all_sides_are_equal(self):
        result = calculate_triangle("5", "5", "5")

        self.assertEqual(result[0], "равносторонний")

    def test_triangle_is_isosceles_when_a_equals_b(self):
        result = calculate_triangle("5", "5", "6")

        self.assertEqual(result[0], "равнобедренный")

    def test_triangle_is_isosceles_when_a_equals_c(self):
        result = calculate_triangle("5", "6", "5")

        self.assertEqual(result[0], "равнобедренный")

    def test_triangle_is_isosceles_when_b_equals_c(self):
        result = calculate_triangle("6", "5", "5")

        self.assertEqual(result[0], "равнобедренный")

    def test_triangle_is_scalene_when_all_sides_are_different(self):
        result = calculate_triangle("3", "4", "5")

        self.assertEqual(result[0], "разносторонний")

    def test_triangle_accepts_fractional_sides(self):
        result = calculate_triangle("2.5", "2.5", "3")

        self.assertEqual(result[0], "равнобедренный")

    def test_triangle_accepts_small_positive_sides(self):
        result = calculate_triangle("0.1", "0.1", "0.1")

        self.assertEqual(result[0], "равносторонний")

    def test_triangle_accepts_large_sides(self):
        result = calculate_triangle("1000000", "1000000", "1000000")

        self.assertEqual(result[0], "равносторонний")

    def test_triangle_returns_three_coordinates(self):
        result = calculate_triangle("3", "4", "5")

        coordinates = result[1]

        self.assertEqual(len(coordinates), 3)

    def test_first_triangle_coordinate_is_5_5(self):
        result = calculate_triangle("3", "4", "5")

        coordinates = result[1]

        self.assertEqual(coordinates[0], (5, 5))

    def test_each_triangle_vertex_has_two_coordinates(self):
        result = calculate_triangle("3", "4", "5")

        coordinates = result[1]

        self.assertEqual(len(coordinates[0]), 2)
        self.assertEqual(len(coordinates[1]), 2)
        self.assertEqual(len(coordinates[2]), 2)

if __name__ == "__main__":
    unittest.main()