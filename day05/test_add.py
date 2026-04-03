import unittest

# 아직 구현하지 않은 함수를 임포트하려고 함
from add import add_numbers

class TestAddNumbers(unittest.TestCase):
    def test_add_two_positive_numbers(self):
        # 2 + 3 = 5를 기대
        self.assertEqual(add_numbers(2, 3), 5)
    
    def test_add_negative_numbers(self):
        # -1 + 1 = 0을 기대
        self.assertEqual(add_numbers(-1, 1), 0)

if __name__ == "__main__":
    unittest.main()