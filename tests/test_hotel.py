from datetime import datetime, date, timedelta

import pytest
import inspect

import app.model.hotel

module_members = [item[0] for item in inspect.getmembers(app.model.hotel)]
guest_defined = "Guest" in module_members
reservation_defined = "Reservation" in module_members
hotel_defined = "Hotel" in module_members
room_defined = "Room" in module_members

if guest_defined:
    from app.model.hotel import Guest

if reservation_defined:
    from app.model.hotel import Reservation

if hotel_defined:
    from app.model.hotel import Hotel

if room_defined:
    from app.model.hotel import Room


base_date = datetime.now().date() + timedelta(days=5)


@pytest.fixture()
def guest_regular():
    return Guest("John Doe", "john@email.com", Guest.REGULAR)


@pytest.fixture()
def guest_vip():
    return Guest("Jane Smith", "jane@email.com", Guest.VIP)


class TestGuest:
    @pytest.mark.skipif(not guest_defined, reason="Guest class not defined")
    def test_guest_class_decorated_with_dataclass(self, guest_regular):
        assert hasattr(guest_regular, "__dataclass_params__")

    @pytest.mark.skipif(not guest_defined, reason="Guest class not defined")
    @pytest.mark.parametrize(
        "constant_name, constant_value", [("REGULAR", "regular"), ("VIP", "vip")]
    )
    def test_guest_class_has_constants_with_value(self, guest_regular, constant_name, constant_value):
        assert hasattr(guest_regular, constant_name)
        assert getattr(guest_regular, constant_name) == constant_value

    @pytest.mark.skipif(not guest_defined, reason="Guest class not defined")
    @pytest.mark.parametrize(
        "attribute_name, attribute_type",
        [("name", str), ("email", str), ("type_", str)]
    )
    def test_guest_class_has_attributes(self, guest_regular, attribute_name, attribute_type):
        assert hasattr(guest_regular, attribute_name)
        assert isinstance(getattr(guest_regular, attribute_name), attribute_type)

    @pytest.mark.skipif(not guest_defined, reason="Guest class not defined")
    def test_guest_class_has_str_method(self, guest_regular):
        assert hasattr(guest_regular, "__str__")
        assert callable(getattr(guest_regular, "__str__"))
        assert isinstance(guest_regular.__str__(), str)

    @pytest.mark.skipif(not guest_defined, reason="Guest class not defined")
    def test_guest_str_method_output(self, guest_regular):
        assert str(guest_regular) == "Guest John Doe (john@email.com) of type regular"


@pytest.fixture()
def reservation_without_guests():
    return Reservation("John Doe",
                       "Business trip",
                       base_date,
                       base_date + timedelta(days=3))


@pytest.fixture()
def reservation_with_guests():
    reservation = Reservation("John Doe",
                              "Business trip",
                              base_date,
                              base_date + timedelta(days=3))
    reservation.add_guest("Jane Smith", "jane@email.com", Guest.VIP)
    reservation.add_guest("Bob Wilson", "bob@email.com", Guest.REGULAR)
    return reservation


class TestReservation:

    @pytest.mark.skipif(not reservation_defined, reason="Reservation class not defined")
    def test_reservation_class_decorated_with_dataclass(self, reservation_without_guests):
        assert hasattr(reservation_without_guests, "__dataclass_params__")

    @pytest.mark.skipif(not reservation_defined, reason="Reservation class not defined")
    @pytest.mark.parametrize(
        "attribute_name, attribute_type",
        [("guest_name", str), ("description", str), ("check_in", date),
         ("check_out", date), ("id", str), ("guests", list)]
    )
    def test_reservation_class_has_attributes(self, reservation_without_guests, attribute_name, attribute_type):
        assert hasattr(reservation_without_guests, attribute_name)
        assert isinstance(getattr(reservation_without_guests, attribute_name), attribute_type)

    @pytest.mark.skipif(not reservation_defined, reason="Reservation class not defined")
    @pytest.mark.parametrize(
        "attribute_name, expected_value",
        [("guest_name", "John Doe"), ("description", "Business trip"),
         ("check_in", base_date),
         ("check_out", base_date + timedelta(days=3)),
         ("id", None),
         ("guests", [])]
    )
    def test_reservation_class_initializes_attributes(self, reservation_without_guests, attribute_name, expected_value):
        if expected_value is not None:
            assert getattr(reservation_without_guests, attribute_name) == expected_value
        else:
            assert getattr(reservation_without_guests, attribute_name)

    @pytest.mark.skipif(not reservation_defined, reason="Reservation class not defined")
    @pytest.mark.parametrize(
        "method_name, expected_return_type, args",
        [("add_guest", None, ("Jane", "jane@email.com", "regular")),
         ("delete_guest", None, (0,)),
         ("__len__", int, ()),
         ("__str__", str, ())]
    )
    def test_reservation_class_has_methods(self, reservation_without_guests, method_name, expected_return_type, args):
        assert hasattr(reservation_without_guests, method_name)
        method = getattr(reservation_without_guests, method_name)
        assert callable(method)
        if expected_return_type:
            assert isinstance(method(*args), expected_return_type)

    @pytest.mark.skipif(not guest_defined, reason="Guest class not defined")
    def test_add_guest_method_functionality(self, reservation_without_guests):
        reservation_without_guests.add_guest("Jane Smith", "jane@email.com", Guest.VIP)
        assert len(reservation_without_guests.guests) == 1
        assert reservation_without_guests.guests[0].type_ == Guest.VIP
        assert reservation_without_guests.guests[0].name == "Jane Smith"
        assert reservation_without_guests.guests[0].email == "jane@email.com"

    @pytest.mark.skipif(not guest_defined, reason="Guest class not defined")
    def test_delete_guest_method_functionality(self, reservation_with_guests):
        reservation_with_guests.delete_guest(0)
        assert len(reservation_with_guests.guests) == 1
        assert reservation_with_guests.guests[0].name == "Bob Wilson"
        assert reservation_with_guests.guests[0].type_ == Guest.REGULAR

    @pytest.mark.skipif(not guest_defined, reason="Guest class not defined")
    def test_delete_guest_method_calls_guest_not_found_error(self, reservation_without_guests):
        with pytest.raises(ValueError):
            reservation_without_guests.delete_guest(0)

    @pytest.mark.skipif(not reservation_defined, reason="Reservation class not defined")
    def test_len_method_returns_number_of_nights(self, reservation_without_guests):
        assert len(reservation_without_guests) == 3

    @pytest.mark.skipif(not reservation_defined, reason="Reservation class not defined")
    def test_len_method_returns_one_for_single_night(self):
        reservation = Reservation("Test", "Test", base_date, base_date + timedelta(days=1))
        assert len(reservation) == 1

    @pytest.mark.skipif(not reservation_defined, reason="Reservation class not defined")
    def test_reservation_class_str_method_output(self, reservation_without_guests):
        reservation_str = str(reservation_without_guests)
        assert f"ID: {reservation_without_guests.id}" in reservation_str
        assert f"Guest: {reservation_without_guests.guest_name}" in reservation_str
        assert f"Description: {reservation_without_guests.description}" in reservation_str
        assert f"Dates: {reservation_without_guests.check_in} - {reservation_without_guests.check_out}" in reservation_str


@pytest.fixture()
def room():
    return Room(101, "single", 100.0)


@pytest.fixture()
def room_with_booking():
    room = Room(101, "single", 100.0)
    room.book("res_id", base_date, base_date + timedelta(days=3))
    return room


class TestRoom:

    @pytest.mark.skipif(not room_defined, reason="Room class not defined")
    def test_room_class_is_not_marked_as_dataclass(self):
        assert not hasattr(Room, "__dataclass_params__")

    @pytest.mark.skipif(not room_defined, reason="Room class not defined")
    @pytest.mark.parametrize(
        "attribute_name, attribute_type",
        [("number", int), ("type_", str), ("price_per_night", float), ("availability", dict)]
    )
    def test_room_class_has_attributes(self, room, attribute_name, attribute_type):
        assert hasattr(room, attribute_name)
        assert isinstance(getattr(room, attribute_name), attribute_type)

    @pytest.mark.skipif(not room_defined, reason="Room class not defined")
    @pytest.mark.parametrize(
        "method_name, expected_return_type, args",
        [("__init__", None, (101, "single", 100.0)),
         ("_init_availability", None, ()),
         ("book", None, ("res_id", base_date + timedelta(days=100), base_date + timedelta(days=101))),
         ("release", None, ("res_id",)),
         ("update_booking", None, ("res_id", base_date + timedelta(days=100), base_date + timedelta(days=101)))]
    )
    def test_room_class_has_methods(self, room, method_name, expected_return_type, args):
        assert hasattr(room, method_name)
        method = getattr(room, method_name)
        assert callable(method)
        if expected_return_type:
            assert isinstance(method(*args), expected_return_type)

    @pytest.mark.skipif(not room_defined, reason="Room class not defined")
    def test_room_class_initializes_availability(self, room):
        today = datetime.now().date()
        assert room.number == 101
        assert room.type_ == "single"
        assert room.price_per_night == 100.0
        assert len(room.availability) == 365
        assert all(v is None for v in room.availability.values())
        assert today in room.availability
        assert today + timedelta(days=364) in room.availability

    @pytest.mark.skipif(not room_defined, reason="Room class not defined")
    def test_book_method_functionality(self, room):
        room.book("res_id", base_date, base_date + timedelta(days=3))
        assert room.availability[base_date] == "res_id"
        assert room.availability[base_date + timedelta(days=1)] == "res_id"
        assert room.availability[base_date + timedelta(days=2)] == "res_id"
        assert room.availability[base_date + timedelta(days=3)] is None

    @pytest.mark.skipif(not room_defined, reason="Room class not defined")
    def test_book_calls_room_not_available_error(self, room_with_booking):
        with pytest.raises(ValueError):
            room_with_booking.book("other_res", base_date, base_date + timedelta(days=2))


@pytest.fixture()
def empty_hotel():
    hotel = Hotel()
    hotel.add_room(101, "single", 100.0)
    hotel.add_room(102, "double", 150.0)
    return hotel


@pytest.fixture()
def hotel_with_reservations():
    hotel = Hotel()
    hotel.add_room(101, "single", 100.0)
    hotel.add_room(102, "double", 150.0)
    hotel.add_room(103, "suite", 300.0)

    reservation = Reservation("John Doe",
                              "Business trip",
                              base_date,
                              base_date + timedelta(days=3),
                              id="res_id")
    hotel.reservations["res_id"] = reservation
    hotel.rooms[101].book("res_id", base_date, base_date + timedelta(days=3))

    hotel.make_reservation("Jane Smith",
                           "Vacation",
                           102,
                           base_date,
                           base_date + timedelta(days=5))
    return hotel


@pytest.fixture()
def hotel_with_partial_availability():
    hotel = Hotel()
    hotel.add_room(101, "single", 100.0)
    hotel.add_room(102, "double", 150.0)
    hotel.add_room(103, "suite", 300.0)

    hotel.make_reservation("Guest A",
                           "Trip A",
                           101,
                           base_date,
                           base_date + timedelta(days=3))

    hotel.make_reservation("Guest B",
                           "Trip B",
                           102,
                           base_date,
                           base_date + timedelta(days=5))

    return hotel


class TestHotel:
    @pytest.mark.skipif(not hotel_defined, reason="Hotel class not defined")
    def test_hotel_class_is_not_marked_as_dataclass(self):
        assert not hasattr(Hotel, "__dataclass_params__")

    @pytest.mark.skipif(not hotel_defined, reason="Hotel class not defined")
    @pytest.mark.parametrize(
        "attribute_name, attribute_type",
        [("rooms", dict), ("reservations", dict)]
    )
    def test_hotel_class_has_attributes(self, empty_hotel, attribute_name, attribute_type):
        assert hasattr(empty_hotel, attribute_name)
        assert isinstance(getattr(empty_hotel, attribute_name), attribute_type)

    @pytest.mark.skipif(not hotel_defined, reason="Hotel class not defined")
    @pytest.mark.parametrize(
        "method_name, expected_return_type, args",
        [("add_room", None, (201, "single", 100.0)),
         ("make_reservation", str, ("Test", "Test desc", 103, base_date + timedelta(days=10), base_date + timedelta(days=11))),
         ("cancel_reservation", None, ("res_id",)),
         ("update_reservation", None, ("res_id", "John", "Trip", 101, base_date, base_date + timedelta(days=3))),
         ("find_reservations", dict, (base_date, base_date + timedelta(days=1))),
         ("add_guest", None, ("res_id", "Jane", "jane@email.com", "regular")),
         ("delete_guest", None, ("res_id", 0)),
         ("list_guests", list, ("res_id",)),
         ("find_available_rooms", list, (base_date + timedelta(days=10), base_date + timedelta(days=11))),
         ("__init__", None, ())]
    )
    def test_hotel_class_has_methods(self, hotel_with_reservations, method_name, expected_return_type, args):
        assert hasattr(hotel_with_reservations, method_name)
        method = getattr(hotel_with_reservations, method_name)
        assert callable(method)
        if expected_return_type:
            assert isinstance(method(*args), expected_return_type)

    @pytest.mark.skipif(not hotel_defined, reason="Hotel class not defined")
    def test_hotel_class_initializes_empty(self):
        hotel = Hotel()
        assert hotel.rooms == {}
        assert hotel.reservations == {}

    @pytest.mark.skipif(not hotel_defined, reason="Hotel class not defined")
    def test_add_room_method_functionality(self):
        hotel = Hotel()
        hotel.add_room(101, "single", 100.0)
        assert 101 in hotel.rooms
        assert hotel.rooms[101].number == 101
        assert hotel.rooms[101].type_ == "single"
        assert hotel.rooms[101].price_per_night == 100.0

    @pytest.mark.skipif(not hotel_defined, reason="Hotel class not defined")
    def test_add_room_method_calls_room_already_exists_error(self, empty_hotel):
        with pytest.raises(ValueError):
            empty_hotel.add_room(101, "double", 200.0)

    @pytest.mark.skipif(not hotel_defined, reason="Hotel class not defined")
    def test_make_reservation_adds_to_dict(self, empty_hotel):
        res_id = empty_hotel.make_reservation("John Doe", "Business trip", 101,
                                              base_date, base_date + timedelta(days=3))
        assert len(empty_hotel.reservations) == 1
        assert res_id in empty_hotel.reservations
        assert empty_hotel.reservations[res_id].guest_name == "John Doe"
        assert empty_hotel.reservations[res_id].description == "Business trip"
        assert empty_hotel.reservations[res_id].check_in == base_date
        assert empty_hotel.reservations[res_id].check_out == base_date + timedelta(days=3)

    @pytest.mark.skipif(not hotel_defined, reason="Hotel class not defined")
    def test_make_reservation_returns_id(self, empty_hotel):
        res_id = empty_hotel.make_reservation("John Doe", "Business trip", 101,
                                              base_date, base_date + timedelta(days=3))
        assert res_id

    @pytest.mark.skipif(not hotel_defined, reason="Hotel class not defined")
    def test_make_reservation_calls_date_lower_than_today_error(self, empty_hotel):
        with pytest.raises(ValueError):
            empty_hotel.make_reservation("John Doe", "Trip", 101,
                                        date(2020, 5, 1), date(2020, 5, 3))

    @pytest.mark.skipif(not hotel_defined, reason="Hotel class not defined")
    def test_make_reservation_calls_room_not_found_error(self, empty_hotel):
        with pytest.raises(ValueError):
            empty_hotel.make_reservation("John Doe", "Trip", 999,
                                        base_date, base_date + timedelta(days=2))

    @pytest.mark.skipif(not hotel_defined, reason="Hotel class not defined")
    def test_make_reservation_books_room(self, empty_hotel):
        res_id = empty_hotel.make_reservation("John Doe", "Trip", 101,
                                              base_date, base_date + timedelta(days=3))
        assert empty_hotel.rooms[101].availability[base_date] == res_id
        assert empty_hotel.rooms[101].availability[base_date + timedelta(days=1)] == res_id
        assert empty_hotel.rooms[101].availability[base_date + timedelta(days=2)] == res_id
        assert empty_hotel.rooms[101].availability[base_date + timedelta(days=3)] is None

    @pytest.mark.skipif(not hotel_defined, reason="Hotel class not defined")
    def test_add_guest_method_functionality(self, hotel_with_reservations):
        hotel_with_reservations.add_guest("res_id", "Bob", "bob@email.com", Guest.VIP)
        assert len(hotel_with_reservations.reservations["res_id"].guests) == 1
        assert hotel_with_reservations.reservations["res_id"].guests[0].name == "Bob"
        assert hotel_with_reservations.reservations["res_id"].guests[0].type_ == Guest.VIP

    @pytest.mark.skipif(not hotel_defined, reason="Hotel class not defined")
    def test_add_guest_calls_reservation_not_found_error(self, hotel_with_reservations):
        with pytest.raises(ValueError):
            hotel_with_reservations.add_guest("nonexistent", "Bob", "bob@email.com", Guest.REGULAR)

    @pytest.mark.skipif(not hotel_defined, reason="Hotel class not defined")
    def test_find_available_rooms_method_functionality(self, hotel_with_partial_availability):
        available = hotel_with_partial_availability.find_available_rooms(
            base_date, base_date + timedelta(days=2))
        assert len(available) == 1
        assert 103 in available
