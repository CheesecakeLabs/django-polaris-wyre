from dataclasses import dataclass
from decimal import Decimal


@dataclass
class TransferData:
    currency: str
    amount: Decimal
    destination: str
