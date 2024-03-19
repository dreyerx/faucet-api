import uuid
from uuid import UUID
from pydantic import BaseModel, Field, UUID4
from datetime import datetime

class RequestClaim(BaseModel):
    address: str

class TransactionModel(BaseModel):
    id:            UUID      = Field(default_factory=uuid.uuid4, alias="_id")
    txhash:        str       = Field(...)
    block:         str       = Field(...)
    to:            str       = Field(...)
    value:         int       = Field(...)
    timestamp:     datetime  = Field(default=datetime.now())