# Hotel Reservation - Class Diagram

```
+--------------------------------------------------+
|                  <<dataclass>>                    |
|                     Guest                         |
+--------------------------------------------------+
| + REGULAR: ClassVar[str] = "regular"              |
| + VIP: ClassVar[str] = "vip"                      |
+--------------------------------------------------+
| + name: str                                       |
| + email: str                                      |
| + type_: str = REGULAR                            |
+--------------------------------------------------+
| + __str__() -> str                                |
+--------------------------------------------------+


+--------------------------------------------------+
|                  <<dataclass>>                    |
|                  Reservation                      |
+--------------------------------------------------+
| + guest_name: str                                 |
| + description: str                                |
| + check_in: date                                  |
| + check_out: date                                 |
| + guests: list[Guest] = []                        |
| + id: str = generate_unique_id()                  |
+--------------------------------------------------+
| + add_guest(name, email, type_) -> None           |
| + delete_guest(guest_index) -> None               |
| + __len__() -> int                                |
| + __str__() -> str                                |
+--------------------------------------------------+
         |
         | +guests  0..*
         v
+--------------------------------------------------+
|                     Guest                         |
+--------------------------------------------------+


+--------------------------------------------------+
|                     Room                          |
+--------------------------------------------------+
| + number: int                                     |
| + type_: str                                      |
| + price_per_night: float                          |
| + availability: dict[date, str | None]            |
+--------------------------------------------------+
| + __init__(number, type_, price_per_night)        |
| - _init_availability() -> None                    |
| + book(reservation_id, check_in, check_out)       |
| + release(reservation_id) -> None                 |
| + update_booking(reservation_id, check_in,        |
|                  check_out) -> None                |
+--------------------------------------------------+


+--------------------------------------------------+
|                     Hotel                         |
+--------------------------------------------------+
| + rooms: dict[int, Room]                          |
| + reservations: dict[str, Reservation]            |
+--------------------------------------------------+
| + __init__()                                      |
| + add_room(number, type_, price_per_night)        |
| + make_reservation(guest_name, description,       |
|      room_number, check_in, check_out) -> str     |
| + cancel_reservation(reservation_id)              |
| + update_reservation(reservation_id, guest_name,  |
|      description, room_number, check_in,          |
|      check_out)                                   |
| + add_guest(reservation_id, name, email, type_)   |
| + delete_guest(reservation_id, guest_index)       |
| + list_guests(reservation_id) -> list[Guest]      |
| + find_available_rooms(check_in, check_out)       |
|      -> list[int]                                 |
| + find_reservations(start_date, end_date)         |
|      -> dict[date, list[Reservation]]             |
+--------------------------------------------------+
         |                    |
         | +rooms  0..*      | +reservations  0..*
         v                    v
      Room              Reservation
```

## Relationships

- **Hotel** `1` --> `0..*` **Room** (role: +rooms)
- **Hotel** `1` --> `0..*` **Reservation** (role: +reservations)
- **Reservation** `1` --> `0..*` **Guest** (role: +guests)
