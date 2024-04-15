from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis import Redis
from config import TIME_LIMIT, REDIS_HOST, REDIS_PORT
from model import RequestClaim
from faucet import claim as ClaimFaucet
from faucet import check_sender_balance
from datetime import timedelta
from datetime import datetime

redis   = Redis(
    REDIS_HOST,
    REDIS_PORT
)
app     = FastAPI()

origins = [
    "http://faucet.dreyerx.com",
    "https://faucet.dreyerx.com",
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
        try:
            tx_faucet     = ClaimFaucet(data.address)
            setCantClaim(data.address)
            next_claim  = datetime.now() + timedelta(seconds=timeClaimAgain)
            return {
                "status": "ok",
                "data": {
                    "transaction_hash": tx_faucet.txhash,
                    "timestamp": tx_faucet.timestamp,
                    "to": tx_faucet.to,
                    "value": tx_faucet.value,
                    "next_claim": next_claim.isoformat()
                }
            }
        except Exception as e:
            return {
                "status": "fail",
                "message": str(e)
            }
    else:
        return {
            "status": "fail",
            "message": f"You can't collect coins now, please wait 24 hours",
            "data": {
                "seconds": timeClaimAgain,
                "timedelta": timedelta(seconds=timeClaimAgain)
            }
        }
    
@app.post("/health")
def health(data: RequestClaim):
    account_balance = check_sender_balance()
    timeClaimAgain = checkClaimedAgain(data.address)
    if timeClaimAgain < 1:
        try:
            if account_balance < 5:
                return {
                    "status": "fail",
                    "message": "The sender's balance is insufficient",
                    "sender_balance": account_balance
                }
            else:
                return {
                    "status": "ok",
                    "message": "ready to use",
                    "sender_balance": account_balance
                }
        except Exception as e:
            return {
                "status": "fail",
                "message": str(e),
                "sender_balance": account_balance
            }
    else:
        return {
            "status": "fail",
            "sender_balance": account_balance,
            "message": f"You can't collect coins now, please wait 24 hours",
            "data": {
                "seconds": timeClaimAgain,
                "timedelta": timedelta(seconds=timeClaimAgain)
            }
        }