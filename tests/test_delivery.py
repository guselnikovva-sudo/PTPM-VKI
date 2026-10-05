import unittest

from Delivery import calculate_delivery_cost


class TestCalculateDeliveryCost(unittest.TestCase):

    def test_normal_package_cost(self):
        result = calculate_delivery_cost(1, 100, "обычный")

        self.assertEqual(result[0], 700)

    def test_minimum_valid_weight(self):
        result = calculate_delivery_cost(0.1, 100, "обычный")

        self.assertNotEqual(result[0], -1)

    def test_weight_below_minimum(self):
        result = calculate_delivery_cost(0.09, 100, "обычный")

        self.assertEqual(result, (-1, "0000-00-00"))

    def test_maximum_valid_weight(self):
        result = calculate_delivery_cost(50.0, 100, "обычный")

        self.assertNotEqual(result[0], -1)

    def test_weight_above_maximum(self):
        result = calculate_delivery_cost(50.01, 100, "обычный")

        self.assertEqual(result, (-1, "0000-00-00"))

    def test_minimum_valid_distance(self):
        result = calculate_delivery_cost(1, 1, "обычный")

        self.assertNotEqual(result[0], -1)

    def test_distance_below_minimum(self):
        result = calculate_delivery_cost(1, 0, "обычный")

        self.assertEqual(result, (-1, "0000-00-00"))

    def test_maximum_valid_distance(self):
        result = calculate_delivery_cost(1, 5000, "обычный")

        self.assertNotEqual(result[0], -1)

    def test_distance_above_maximum(self):
        result = calculate_delivery_cost(1, 5001, "обычный")

        self.assertEqual(result, (-1, "0000-00-00"))

    def test_fragile_package_adds_300(self):
        result = calculate_delivery_cost(1, 100, "хрупкий")

        self.assertEqual(result[0], 1000)

    def test_express_delivery_should_not_be_cheaper_than_normal(self):
        normal_result = calculate_delivery_cost(1, 100, "обычный", False)
        express_result = calculate_delivery_cost(1, 100, "обычный", True)

        self.assertGreater(express_result[0], normal_result[0])

    def test_express_delivery_should_take_at_least_one_day(self):
        result = calculate_delivery_cost(1, 100, "обычный", True)

        self.assertEqual(result[1], "2026-09-04")

if __name__ == "__main__":
    unittest.main()