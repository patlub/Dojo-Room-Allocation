import unittest
from classes.office import Office

class OfficeTestCase(unittest.TestCase):

    def setUp(self):
        self.office = Office()

    def test_something(self):
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
