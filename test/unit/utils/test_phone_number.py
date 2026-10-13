"""
test_phone_number.py

Unit tests for the phone number utilities

@copyright Bandwidth Inc.
"""
import unittest

from bandwidth.utils import (
    InvalidPhoneNumberError,
    is_valid_e164,
    normalize_us_number,
    to_e164,
)


class TestIsValidE164(unittest.TestCase):

    def test_valid_numbers(self):
        for number in ["+19195551234", "+442071838750", "+12"]:
            with self.subTest(number=number):
                assert is_valid_e164(number)

    def test_invalid_numbers(self):
        for number in ["19195551234", "+0123456789", "+1 919 555 1234",
                       "+1234567890123456", "", None, 19195551234]:
            with self.subTest(number=number):
                assert not is_valid_e164(number)


class TestNormalizeUsNumber(unittest.TestCase):

    def test_common_formats(self):
        for number in ["(919) 555-1234", "919.555.1234", "9195551234",
                       "1-919-555-1234", "+1 919 555 1234"]:
            with self.subTest(number=number):
                assert normalize_us_number(number) == "+19195551234"

    def test_wrong_length(self):
        with self.assertRaises(InvalidPhoneNumberError):
            normalize_us_number("555-1234")

    def test_invalid_area_code(self):
        with self.assertRaises(InvalidPhoneNumberError):
            normalize_us_number("019-555-1234")

    def test_invalid_exchange_code(self):
        with self.assertRaises(InvalidPhoneNumberError):
            normalize_us_number("919-155-1234")

    def test_non_string(self):
        with self.assertRaises(InvalidPhoneNumberError):
            normalize_us_number(9195551234)


class TestToE164(unittest.TestCase):

    def test_already_e164(self):
        assert to_e164("+442071838750") == "+442071838750"

    def test_strips_formatting_after_plus(self):
        assert to_e164("+44 20 7183 8750") == "+442071838750"

    def test_default_us(self):
        assert to_e164("(919) 555-1234") == "+19195551234"

    def test_other_country_code(self):
        assert to_e164("2071838750", default_country_code="44") == "+442071838750"

    def test_invalid(self):
        with self.assertRaises(InvalidPhoneNumberError):
            to_e164("+0000")


if __name__ == '__main__':
    unittest.main()
