import unittest
from classes.dojo import Dojo


class TestClassDojo(unittest.TestCase):
    def test_create_room_successfully(self):
        dojo = Dojo()
        initial_office_count = len(dojo.all_offices)
        blue_office = dojo.create_room('Blue', 'office')
        # self.assertTrue(blue_office)
        new_office_count = len(dojo.all_offices)
        self.assertEqual(new_office_count - initial_office_count, 1)

if __name__ == '__main__':
    unittest.main()