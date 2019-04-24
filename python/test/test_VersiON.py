import unittest

from version.VersiON import VersiON


class TestSum(unittest.TestCase):

    def test_Should_fail_match_style_When_unknown_version_name_passed(self):
        with self.assertRaises(Exception):
            VersiON('test', 'unknown_style', None)

    def test_Should_fail_match_style_When_None_version_name_passed(self):
        with self.assertRaises(Exception):
            VersiON('test', None, None)


if __name__ == '__main__':
    unittest.main()
