import unittest

class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.number = 10
    
    def test_addition(self):
        self.assertEqual(1 + 1, 2)

    def test_addition_with_number(self):
        self.assertEqual(self.number + 5, 15)

    def tearDown(self):
        del self.number

if __name__ == "__main__":
    unittest.main()


