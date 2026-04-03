def add_numbers(a, b):
    return a + b

def test_add_with_invalid_input(self):
    # 문자열을 넣으면 TypeError를 기대
    with self.assertRaises(TypeError):
        add_numbers("two", 3)