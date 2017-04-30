import unittest
from classes.dojo import Dojo
from classes.dojo import Fellow


class TestClassDojo(unittest.TestCase):
    def setUp(self):
        self.dojo = Dojo()

    def test_create_offices_successfully(self):
        office_name_list = ['blue', 'red']
        self.dojo.create_room(office_name_list, 'office')
        size  = len(self.dojo.all_offices)
        self.assertEqual(self.dojo.all_offices[size-1].name,  'red')
        self.assertEqual(self.dojo.all_offices[size-2].name,  'blue')

    def test_create_living_space_successfully(self):
        living_space_name_list = ['Apple', 'Mango']
        self.dojo.create_room(living_space_name_list, 'living_space')
        size = len(self.dojo.all_living_spaces)
        self.assertEqual(self.dojo.all_living_spaces[size - 1].name, 'Mango')
        self.assertEqual(self.dojo.all_living_spaces[size - 2].name, 'Apple')

    def tests_get_available_office(self):
        office_name_list = ['blue']
        self.dojo.create_room(office_name_list, 'office')
        self.dojo.all_offices[0].spaces = 0
        self.assertFalse(self.dojo.get_available_office())

    def tests_get_available_office_with_no_space(self):
        office_name_list = ['blue', 'red']
        self.dojo.create_room(office_name_list, 'office')
        self.assertTrue(self.dojo.get_available_office(), True)

    def tests_add_person_to_room_type_living_space(self):
        room_name_list = ['blue']
        self.dojo.create_room(room_name_list, 'living_space')
        fellow = Fellow('Patrick')
        room = self.dojo.get_available_living_spaces()
        self.dojo.add_person_to_room(fellow, room)
        self.assertEqual(room.occupants[0].name, 'Patrick')

    def tests_add_person_to_room_type_office(self):
        room_name_list = ['blue']
        self.dojo.create_room(room_name_list, 'office')
        fellow = Fellow('Patrick')
        room = self.dojo.get_available_office()
        self.dojo.add_person_to_room(fellow, room)
        self.assertEqual(room.occupants[0].name, 'Patrick')


    def test_create_room_with_empty_string(self):
        self.assertRaises(ValueError, self.dojo.create_room, [], "")

    def test_create_room_with_wrong_argument_types(self):
        self.assertRaises(TypeError, self.dojo.create_room, 5, 9)

    def test_create_fellow_successfully_without_accomodation_specified(self):
        initial_fellow_count = len(self.dojo.all_fellows)
        self.dojo.add_fellow('name')
        new_fellow_count = len(self.dojo.all_fellows)
        self.assertEqual(new_fellow_count - initial_fellow_count, 1)

    def test_create_fellow_successfully_with_accomodation(self):
        initial_fellow_count = len(self.dojo.all_fellows)
        self.dojo.add_fellow('name', 'Y')
        new_fellow_count = len(self.dojo.all_fellows)
        self.assertEqual(new_fellow_count - initial_fellow_count, 1)

    def test_create_fellow_successfully_without_accomodation(self):
        initial_fellow_count = len(self.dojo.all_fellows)
        self.dojo.add_fellow('name', 'N')
        new_fellow_count = len(self.dojo.all_fellows)
        self.assertEqual(new_fellow_count - initial_fellow_count, 1)

    def test_create_staff_successfully_without_accomodation(self):
        initial_staff_count = len(self.dojo.all_staff)
        self.dojo.add_staff('name')
        new_staff_count = len(self.dojo.all_staff)
        self.assertEqual(new_staff_count - initial_staff_count, 1)

    def test_create_staff_with_accomodation(self):
        initial_staff_count = len(self.dojo.all_staff)
        self.assertEqual(self.dojo.add_staff('name', 'Y'), 'Staff can not have accomodation')

    def test_available_space_after_adding_fellow_to_office(self):
        office_name_list = ['blue']
        self.dojo.create_room(office_name_list, 'office')
        self.dojo.add_fellow('name')
        self.dojo.add_fellow('name2')
        self.dojo.add_fellow('name3')
        self.dojo.add_fellow('name4')
        office = self.dojo.add_fellow('name5')
        self.assertTrue(office.contains_space())

    def test_space_not_available_after_adding_fellow_to_office(self):
        office_name_list = ['blue']
        self.dojo.create_room(office_name_list, 'office')
        self.dojo.add_fellow('name')
        self.dojo.add_fellow('name2')
        self.dojo.add_fellow('name3')
        self.dojo.add_fellow('name4')
        self.dojo.add_fellow('name5')
        self.dojo.add_fellow('name5')
        office = self.dojo.add_fellow('name5')
        # self.assertEqual(office.spaces, 0)
        self.assertFalse(office.contains_space())

    def test_unallocated_fellows_if_office_space_runs_out(self):
        office_name_list = ['blue']
        self.dojo.create_room(office_name_list, 'office')
        self.dojo.add_fellow('name')
        self.dojo.add_fellow('name2')
        self.dojo.add_fellow('name3')
        self.dojo.add_fellow('name4')
        self.dojo.add_fellow('name5')
        self.dojo.add_fellow('name6')
        self.dojo.add_fellow('name7')
        self.assertEqual(len(self.dojo.fellows_not_allocated_office), 1)
        self.dojo.add_fellow('name8')
        self.assertEqual(len(self.dojo.fellows_not_allocated_office), 2)

    def test_unallocated_fellows_if_living_space_runs_out(self):
        office_name_list = ['blue']
        self.dojo.create_room(office_name_list, 'living_space')
        self.dojo.add_fellow('name1', 'Y')
        self.dojo.add_fellow('name2', 'Y')
        self.dojo.add_fellow('name3', 'Y')
        self.dojo.add_fellow('name4', 'Y')
        self.dojo.add_fellow('name5', 'Y')
        self.dojo.add_fellow('name6', 'Y')
        self.dojo.add_fellow('name7', 'Y')
        self.assertEqual(len(self.dojo.fellows_not_allocated_living_space), 3)
        self.dojo.add_fellow('name8', 'Y')
        self.assertEqual(len(self.dojo.fellows_not_allocated_living_space), 4)

    def test_re_allocate_person(self):
        office_name_list = ['blue']
        self.dojo.create_room(office_name_list, 'office')
        self.dojo.add_fellow('Patrick')
        person = self.dojo.get_person('Patrick')
        self.assertEqual(person.office.name, 'blue')
        office_name_list = ['red']
        self.dojo.create_room(office_name_list, 'office')
        self.dojo.re_allocate_person('Patrick', 'red')
        person = self.dojo.get_person('Patrick')
        self.assertEqual(person.office.name, 'red')

    def test_check_occupants_in_room_when_person_reallocates(self):
        office_name_list = ['blue']
        self.dojo.create_room(office_name_list, 'office')
        self.dojo.add_fellow('Patrick')
        person = self.dojo.get_person('Patrick')
        room = self.dojo.get_room('blue')
        self.assertEqual(room.occupants[0], person)
        office_name_list = ['red']
        self.dojo.create_room(office_name_list, 'office')
        self.dojo.re_allocate_person('Patrick', 'red')
        person = self.dojo.get_person('Patrick')
        room = self.dojo.get_room('red')
        self.assertEqual(room.occupants[0], person)

    def test_re_allocate_person_when_room_does_not_exist(self):
        office_name_list = ['blue', 'orange']
        self.dojo.create_room(office_name_list, 'office')
        self.assertEqual(self.dojo.re_allocate_person('Patrick','yellow'), 'Room with name yellow does not exist')

    def test_re_allocate_person_when_person_does_not_exist(self):
        office_name_list = ['blue', 'orange']
        self.dojo.create_room(office_name_list, 'office')
        self.dojo.add_fellow('Jim')
        self.assertEqual(self.dojo.re_allocate_person('Patrick','blue'), 'Person with name Patrick does not exist')

    def test_re_allocate_person_to_living_room(self):
        office_name_list = ['blue']
        self.dojo.create_room(office_name_list, 'office')
        self.dojo.add_staff('Samuel')
        self.dojo.create_room(['orange'], 'living_space')
        self.assertEqual(self.dojo.re_allocate_person('Samuel','orange'), 'Cant Re-allocate staff to a living room')

    def test_loads_people_from_file(self):
        init_number_of_fellows = len(self.dojo.all_fellows)
        init_number_of_staff = len(self.dojo.all_staff)
        self.dojo.load_people('../files/test.txt')
        final_number_of_fellows = len(self.dojo.all_fellows)
        final_number_of_staff = len(self.dojo.all_staff)
        self.assertEqual(4, final_number_of_fellows - init_number_of_fellows)
        self.assertEqual(3, final_number_of_staff - init_number_of_staff)

    def test_add_fellow_with_junk_name(self):
        self.assertEqual(self.dojo.add_fellow('&%$#&', 'fellow'), 'Please use a valid room name')

    def test_create_fellow_with_empty_string(self):
        self.assertRaises(ValueError, self.dojo.add_fellow, "", "")

    def test_create_fellow_with_non_strings(self):
        self.assertRaises(ValueError, self.dojo.add_fellow(), 5, 9)

if __name__ == '__main__':
    unittest.main()
