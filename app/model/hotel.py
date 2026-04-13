from dataclasses import dataclass, field


@dataclass
class Guest:
    REGULAR = "regular"
    VIP = "vip"

    name: str
    email: str
    type_: str = REGULAR

    def __str__(self) -> str:
        return f"Guest {self.name} ({self.email}) of type {self.type_}"