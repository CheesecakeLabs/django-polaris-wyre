from dataclasses import dataclass
from decimal import Decimal


@dataclass
class TransferData:
    currency: str
    amount: Decimal
    destination: str

    @classmethod
    def create_transfer_data(cls, *args, **kwargs) -> "TransferData":
        return cls(*args, **kwargs)
