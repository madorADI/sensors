import unittest
from id_auth import fill_id, get_auth_digit, is_valid_id


class test_id_auth(unittest.TestCase):
    def test_fill_id_norm(self):
        actual = fill_id("123")
        excepted = "000000123"
        self.assertEqual(actual, excepted)

    def test_fill_id_zero(self):
        actual = fill_id("123", 0)
        excepted = "123"
        self.assertEqual(actual, excepted)

    def test_fill_id_negative(self):
        actual = fill_id("123", -4)
        excepted = "0123"
        self.assertEqual(actual, excepted)

    def test_auth_digit_norm(self):
        actual = get_auth_digit("00000123")
        excepted = 0
        self.assertEquals(actual, excepted)

    def test_auth_digit_error(self):
        with self.assertRaises(ValueError):
            actual = get_auth_digit("1")

    def test_valid_norm(self):
        actual = is_valid_id("326281367")
        excepted = True
        self.assertEquals(actual, excepted)

    def test_valid_error(self):
        with self.assertRaises(ValueError):
            actual = is_valid_id("111111111111111")

    def test_valid_with_filler(self):
        actual = is_valid_id("12344")
        excepted = True
        self.assertEquals(actual, excepted)

    def test_invalid_norm(self):
        actual = is_valid_id("326281361")
        excepted = False
        self.assertEquals(actual, excepted)

    def test_invalid_with_filler(self):
        actual = is_valid_id("1234")
        excepted = False
        self.assertEquals(actual, excepted)


unittest.main()
