import pickle

from app.model.hotel import Hotel


class PersistenceService:
    def __init__(self, file_path: str):
        self.file_path: str = file_path

    def save(self, hotel: Hotel):
        with open(self.file_path, mode="wb") as file:
            pickle.dump(hotel, file)

    def load(self) -> Hotel:
        with (open(self.file_path, mode="rb") as file):
            try:
                hotel = pickle.load(file)
            except EOFError:
                hotel = Hotel()
        return hotel
