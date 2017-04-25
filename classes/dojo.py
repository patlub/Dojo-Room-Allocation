from classes.room import Room


class Dojo:
    def __init__(self):
        self.all_offices = []
        self.all_living_places = []

    def create_room(self, room_name, room_type):
        if room_type == 'office':
            office = Office(name)
            self.all_offices.append(room_name)

        else:
            living_place = LivingPlace(name)
            self.all_living_places.append(room_name)



    