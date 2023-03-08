import unittest
import borderCheck



class TestBorderCheck(unittest.TestCase):
    def test_location_in_border(self):
        result = borderCheck.changeLocation_rect(0, 30, 0, 30, 1, 4, 5, 0, 0, 5, 5)
        self.assertEqual(
            result, ("location changed successfully", 9, 10), "ASSERT IS WRONG"
        )

    def test_location_y_out_of_min_limit(self):
        result = borderCheck.changeLocation_rect(0, 30, 0, 30, 0.1, 4, 5, 0, 1, 5, 4)
        self.assertEqual(
            result,
            "new location is out of borders, no changes were made",
            "ASSERT IS WRONG",
        )

    def test_location_x_out_of_min_limit(self):
        result = borderCheck.changeLocation_rect(0, 30, 0, 30, 0.1, 5, 4, 1, 0, 4, 5)
        self.assertEqual(
            result,
            "new location is out of borders, no changes were made",
            "ASSERT IS WRONG",
        )

    def test_location_y_out_of_max_limit(self):
        result = borderCheck.changeLocation_rect(0, 30, 0, 30, 0.1, 4, 5, 0, 0, 5, 28)
        self.assertEqual(
            result,
            "new location is out of borders, no changes were made",
            "ASSERT IS WRONG",
        )

    def test_location_x_out_of_max_limit(self):
        result = borderCheck.changeLocation_rect(0, 30, 0, 30, 0.1, 4, 5, 0, 0, 28, 5)
        self.assertEqual(
            result,
            "new location is out of borders, no changes were made",
            "ASSERT IS WRONG",
        )

    def test_location_both_out_of_limit(self):
        result = borderCheck.changeLocation_rect(0, 30, 0, 30, 0.1, 4, 6, 0, 1, 28, 5)
        self.assertEqual(
            result,
            "new location is out of borders, no changes were made",
            "ASSERT IS WRONG",
        )


unittest.main(argv=[""], exit=False)


# min_limit_x, max_limit_x, min_limit_y, max_limit_y, sleep_time, x_change, y_change, x_dir, y_dir, location_x, location_y
