from pydantic import BaseModel
from dataclasses import dataclass, asdict
from datetime import datetime

class RequestClaim(BaseModel):
    address: str

@dataclass
class TransactionModel:
    txhash:        str
    block:         str
    timestamp:     str
    to:            str
    value:         str