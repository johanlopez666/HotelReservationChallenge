import argparse
import shlex
from datetime import date, datetime
from importlib.resources import files
from pathlib import Path

from app.model.hotel import Hotel
from app.services.persistence import PersistenceService


class ConsoleView:
    def __init__(self, hotel: Hotel = None):
        file_path = str(files("app").joinpath(Path("data/hotel.data")))
        self.persistence_service: PersistenceService = PersistenceService(file_path)
        if not hotel:
            self.hotel: Hotel = self.persistence_service.load()
        else:
            self.hotel: Hotel = hotel

    @staticmethod
    def show_welcome_msg():
        print(f"{'=' * 40}")
        print("WELCOME TO THE HOTEL RESERVATION APP")
        print(f"{'=' * 40}")
        print("To view the list of commands, type 'help'")

    @staticmethod
    def show_help(command: str | None = None):
        if not command:
            print("\nCOMMANDS:")
            print("help - view the list of commands. Use help <command> to view the help message for a "
                  "specific command")
            print("add_room - add a new room to the hotel")
            print("make_reservation - make a new reservation")
            print("update_reservation - update a reservation")
            print("cancel_reservation - cancel a reservation")
            print("find_reservations - find reservations in a specific date range")
            print("add_guest - add a guest to a reservation")
            print("delete_guest - delete a guest from a reservation")
            print("list_guests - list all guests of a reservation")
            print("available_rooms - list all available rooms for a date range")
            print("exit - close the application")
        else:
            match command:
                case "help":
                    print("help <command> - view the help message for a specific command")
                case "add_room":
                    print("Add a new room to the hotel")
                    print("Usage: add_room <number> <type> <price_per_night>")
                    print("Example: add_room 101 single 100.0")
                case "make_reservation":
                    print("Make a new reservation")
                    print("Usage: make_reservation <guest_name> <description> <room_number> <check_in> <check_out>")
                    print("Example: make_reservation 'John Doe' 'Business trip' 101 2025-10-15 2025-10-18")
                case "update_reservation":
                    print("Update an existing reservation")
                    print("Usage: update_reservation <reservation_id> <guest_name> <description> <room_number> <check_in> <check_out>")
                    print("Example: update_reservation abc12 'John Doe' 'Extended trip' 101 2025-10-15 2025-10-20")
                case "cancel_reservation":
                    print("Cancel a reservation")
                    print("Usage: cancel_reservation <reservation_id>")
                    print("Example: cancel_reservation abc12")
                case "find_reservations":
                    print("List all reservations in a specific date range")
                    print("Usage: find_reservations <start_date> <end_date>")
                    print("Example: find_reservations 2025-10-15 2025-10-20")
                case "add_guest":
                    print("Add a guest to a reservation of type 'regular' or 'vip'")
                    print("Usage: add_guest <reservation_id> <name> <email> <type>")
                    print("Example: add_guest abc12 'Jane Smith' 'jane@email.com' vip")
                case "delete_guest":
                    print("Delete a guest from a reservation")
                    print("Usage: delete_guest <reservation_id> <guest_index>")
                    print("Example: delete_guest abc12 1")
                case "list_guests":
                    print("List all guests of a reservation")
                    print("Usage: list_guests <reservation_id>")
                    print("Example: list_guests abc12")
                case "available_rooms":
                    print("List all available rooms for a date range")
                    print("Usage: available_rooms <check_in> <check_out>")
                    print("Example: available_rooms 2025-10-15 2025-10-18")
                case _:
                    print(f">>> ERROR: command {command} not supported. Type 'help' to view the list of commands")

    def add_room(self, args):
        try:
            self.hotel.add_room(args.number,
                                args.type,
                                args.price_per_night)
        except ValueError as e:
            print(f">>> ERROR: {e}")
        else:
            print(f"Room {args.number} added successfully")

    def make_reservation(self, args):
        try:
            res_id = self.hotel.make_reservation(args.guest_name,
                                                 args.description,
                                                 args.room_number,
                                                 datetime.strptime(args.check_in, '%Y-%m-%d').date(),
                                                 datetime.strptime(args.check_out, '%Y-%m-%d').date())
        except ValueError as e:
            print(f">>> ERROR: {e}")
        else:
            print(f"Reservation created successfully with id {res_id}")

    def update_reservation(self, args):
        try:
            self.hotel.update_reservation(args.reservation_id,
                                          args.guest_name,
                                          args.description,
                                          args.room_number,
                                          datetime.strptime(args.check_in, '%Y-%m-%d').date(),
                                          datetime.strptime(args.check_out, '%Y-%m-%d').date())
        except ValueError as e:
            print(f">>> ERROR: {e}")
        else:
            print("Reservation updated successfully")

    def cancel_reservation(self, args):
        try:
            self.hotel.cancel_reservation(args.reservation_id)
        except ValueError as e:
            print(f">>> ERROR: {e}")
        else:
            print("Reservation cancelled successfully")

    def find_reservations(self, args):
        reservations = self.hotel.find_reservations(
            datetime.strptime(args.start_date, '%Y-%m-%d').date(),
            datetime.strptime(args.end_date, '%Y-%m-%d').date())
        if reservations:
            for date_, reservations_ in reservations.items():
                print(f"Reservations on {date_}:")
                for reservation in reservations_:
                    print(reservation)
                    print()
                print()
        else:
            print("No reservations found")

    def add_guest(self, args):
        try:
            self.hotel.add_guest(args.reservation_id,
                                 args.name,
                                 args.email,
                                 args.type)
        except ValueError as e:
            print(f">>> ERROR: {e}")
        else:
            print("Guest added successfully")

    def delete_guest(self, args):
        try:
            self.hotel.delete_guest(args.reservation_id, args.guest_index - 1)
        except ValueError as e:
            print(f">>> ERROR: {e}")
        else:
            print("Guest deleted successfully")

    def list_guests(self, args):
        guests = self.hotel.list_guests(args.reservation_id)
        if guests:
            for i, guest in enumerate(guests, start=1):
                print(f"{i}. {guest}")
        else:
            print("No guests found")

    def find_available_rooms(self, args):
        available_rooms = self.hotel.find_available_rooms(
            datetime.strptime(args.check_in, '%Y-%m-%d').date(),
            datetime.strptime(args.check_out, '%Y-%m-%d').date())
        if available_rooms:
            print(f"Available rooms from {args.check_in} to {args.check_out}:")
            for room_number in available_rooms:
                room = self.hotel.rooms[room_number]
                print(f"- Room {room.number} ({room.type_}) - ${room.price_per_night}/night")
        else:
            print("No available rooms found")

    def save_hotel(self):
        self.persistence_service.save(self.hotel)

    def process_user_command(self, user_input: str) -> bool:
        line = shlex.split(user_input)
        command = line[0]
        params = line[1:]
        parser = argparse.ArgumentParser()
        match command:
            case "help":
                if params:
                    parser.add_argument("command", type=str, help="Command to view help message for")
                    args = parser.parse_args(params)
                    self.show_help(args.command)
                else:
                    self.show_help()
            case "add_room":
                parser.add_argument("number", type=int, help="Room number")
                parser.add_argument("type", type=str, help="Room type (single, double, suite)")
                parser.add_argument("price_per_night", type=float, help="Price per night")
                args = parser.parse_args(params)
                self.add_room(args)
            case "make_reservation":
                parser.add_argument("guest_name", type=str, help="Guest name")
                parser.add_argument("description", type=str, help="Reservation description")
                parser.add_argument("room_number", type=int, help="Room number")
                parser.add_argument("check_in", type=str, help="Check-in date")
                parser.add_argument("check_out", type=str, help="Check-out date")
                args = parser.parse_args(params)
                self.make_reservation(args)
            case "update_reservation":
                parser.add_argument("reservation_id", type=str, help="Reservation id")
                parser.add_argument("guest_name", type=str, help="Guest name")
                parser.add_argument("description", type=str, help="Reservation description")
                parser.add_argument("room_number", type=int, help="Room number")
                parser.add_argument("check_in", type=str, help="Check-in date")
                parser.add_argument("check_out", type=str, help="Check-out date")
                args = parser.parse_args(params)
                self.update_reservation(args)
            case "cancel_reservation":
                parser.add_argument("reservation_id", type=str, help="Reservation id")
                args = parser.parse_args(params)
                self.cancel_reservation(args)
            case "find_reservations":
                parser.add_argument("start_date", type=str, help="Start date")
                parser.add_argument("end_date", type=str, help="End date")
                args = parser.parse_args(params)
                self.find_reservations(args)
            case "add_guest":
                parser.add_argument("reservation_id", type=str, help="Reservation id")
                parser.add_argument("name", type=str, help="Guest name")
                parser.add_argument("email", type=str, help="Guest email")
                parser.add_argument("type", type=str, help="Guest type: regular or vip")
                args = parser.parse_args(params)
                self.add_guest(args)
            case "delete_guest":
                parser.add_argument("reservation_id", type=str, help="Reservation id")
                parser.add_argument("guest_index", type=int, help="Guest index")
                args = parser.parse_args(params)
                self.delete_guest(args)
            case "list_guests":
                parser.add_argument("reservation_id", type=str, help="Reservation id")
                args = parser.parse_args(params)
                self.list_guests(args)
            case "available_rooms":
                parser.add_argument("check_in", type=str, help="Check-in date")
                parser.add_argument("check_out", type=str, help="Check-out date")
                args = parser.parse_args(params)
                self.find_available_rooms(args)
            case "exit":
                self.save_hotel()
                return True
            case _:
                print(">>> ERROR: Invalid command. Type 'help' to view the list of commands")

    def app_loop(self):
        ConsoleView.show_welcome_msg()
        end_app: bool = False
        while not end_app:
            user_input: str = input("\nHotelApp > ")
            end_app = self.process_user_command(user_input)
