import random
from datetime import datetime
from config import RPC_URL, WALLET, VALUE
from web3 import Web3, HTTPProvider
from web3.types import TxParams
from eth_account.signers.local import LocalAccount
from model import TransactionModel

provider    = Web3(
    HTTPProvider(
        RPC_URL
    )
)

def claim(target):
    account: LocalAccount    = provider.eth.account.from_key(
        random.choice(WALLET)
    )
    transaction: TxParams = {
        "from": account.address,
        "to": target,
        "value": provider.to_wei(VALUE, "ether"),
        "nonce": provider.eth.get_transaction_count(account.address)
    }
    tx_hash     = provider.eth.send_transaction(
        transaction
    )
    tx_data     = provider.eth.get_transaction_receipt(tx_hash)
    tx_model     = TransactionModel(
        txhash=tx_data.get("transactionHash").hex(),
        block=str(tx_data.get("blockNumber")),
        to=tx_data.get("to"),
        value=provider.to_wei(VALUE, "ether")
    )
    return tx_model