import unittest
from classes.dojo import Dojo


class TestClassDojo(unittest.TestCase):
    def setUp(self):
        self.dojo = Dojo()

    def test_create_offices_successfully(self):
        office_name_list = ['blue', 'red']
        initial_office_count = len(self.dojo.all_offices)
        self.dojo.create_room(office_name_list, 'office')
        new_office_count = len(self.dojo.all_offices)
        self.assertEqual(new_office_count - initial_office_count, 2)

    def test_create_living_space_successfully(self):
        living_space_name_list = ['blue', 'red']
        initial_living_space_count = len(self.dojo.all_living_spaces)
        self.dojo.create_room(living_space_name_list, 'living_space')
        new_living_space_count = len(self.dojo.all_living_spaces)
        self.assertEqual(new_living_space_count - initial_living_space_count, 2)

    def test_create_room_with_empty_string(self):
        self.assertRaises(ValueError, self.dojo.create_room, [], "")

    def test_create_room_with_wrong_argument_types(self):
        self.assertRaises(TypeError, self.dojo.create_room, 5, 9)

    # def test_create_room_with_junk_name(self):
    #     self.assertEqual(self.dojo.create_room, 'Please use a valid room name')

    def test_create_fellow_successfully_without_accomodation_specified(self):
        initial_fellow_count = len(self.dojo.all_fellows)
        self.dojo.add_fellow('name')
        new_fellow_count = len(self.dojo.all_fellows)
        self.assertEqual(new_fellow_count - initial_fellow_count, 1)
    #
    def test_create_fellow_successfully_with_accomodation(self):
        initial_fellow_count = len(self.dojo.all_fellows)
        self.dojo.add_fellow('name', 'Y')
        new_fellow_count = len(self.dojo.all_fellows)
        self.assertEqual(new_fellow_count - initial_fellow_count, 1)
    #
    def test_create_fellow_successfully_without_accomodation(self):
        initial_fellow_count = len(self.dojo.all_fellows)
        self.dojo.add_fellow('name', 'N')
        new_fellow_count = len(self.dojo.all_fellows)
        self.assertEqual(new_fellow_count - initial_fellow_count, 1)
    #
    def test_create_staff_successfully_without_accomodation(self):
        initial_staff_count = len(self.dojo.all_staff)
        self.dojo.add_staff('name')
        new_staff_count = len(self.dojo.all_staff)
        self.assertEqual(new_staff_count - initial_staff_count, 1)
    #
    def test_create_staff_with_accomodation(self):
        initial_staff_count = len(self.dojo.all_staff)
        self.assertEqual(self.dojo.add_staff('name', 'Y'), 'Staff can not have accomodation')
    #
    # def test_add_fellow_with_junk_name(self):
    #     self.assertEqual(self.dojo.add_fellow('&%$#&', 'fellow'), 'Please use a valid room name')
    #
    # def test_create_fellow_with_empty_string(self):
    #     self.assertRaises(ValueError, self.dojo.add_fellow, "", "")
    #
    # def test_create_fellow_with_non_strings(self):
    #     self.assertRaises(ValueError, self.dojo.add_fellow(), 5, 9)

        # def test_get_available_office(self):
        #     self.dojo.add_fellow('Patrick', 'Y')
        #     self.assertEqual()


if __name__ == '__main__':
    unittest.main()