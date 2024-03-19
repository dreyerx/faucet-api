from typing import Union
from fastapi import FastAPI
from redis import Redis
from config import TIME_LIMIT, REDIS_HOST, REDIS_PORT
from model import RequestClaim
from faucet import claim as ClaimFaucet
from database import Database

redis   = Redis(
    REDIS_HOST,
    REDIS_PORT
)
app     = FastAPI()
database    = Database()

def checkClaimedAgain(address: str):
    ttl     = redis.ttl(f"faucet_{address}")
    if ttl < 1: return 0
    return ttl

def setCantClaim(address: str):
    redis.set(f"faucet_{address}", "1", TIME_LIMIT)

@app.post("/claim")
def claim(data: RequestClaim):
    timeClaimAgain  = checkClaimedAgain(data.address)
    if timeClaimAgain < 1:
        tx_faucet     = ClaimFaucet(data.address)
        database.save_transaction(tx_faucet)
        setCantClaim(data.address)
        return {
            "status": "ok",
            "data": {
                "transaction_hash": tx_faucet.txhash,
                "block": tx_faucet.block,
                "timestamp": tx_faucet.timestamp,
                "to": tx_faucet.to,
                "value": tx_faucet.value
            }
        }
    else:
        return {
            "status": "fail",
            "message": f"Claim failed, you can claim again in {timeClaimAgain} seconds"
        }

@app.get("/transactions")
def transactions(limit: int = 100):
    return {"limit": limit}