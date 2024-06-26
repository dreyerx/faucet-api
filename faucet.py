import random
from datetime import datetime
from config import RPC_URL, WALLET, VALUE
from web3 import Web3, HTTPProvider
from web3.types import TxParams
from web3.middleware import geth_poa
from eth_account.signers.local import LocalAccount
from model import TransactionModel

provider = Web3(
    HTTPProvider(
        RPC_URL
    )
)

provider.middleware_onion.inject(geth_poa.geth_poa_middleware, layer=0)

def claim(target):
    if provider.is_address(target) is False:
        raise Exception("Invalid ethereum address")
    target_checksum = provider.to_checksum_address(target)
    account: LocalAccount = provider.eth.account.from_key(
        WALLET
    )
    transaction: TxParams = {
        "chainId": 23452,
        "from": account.address,
        "to": target_checksum,
        "value": provider.to_wei(VALUE, "ether"),
        "nonce": provider.eth.get_transaction_count(account.address),
        "gas": 200000,
        "gasPrice": provider.eth.gas_price
    }
    tx = provider.eth.account.sign_transaction(
        transaction,
        account.key
    )
    tx_hash = provider.eth.send_raw_transaction(tx.rawTransaction)
    tx_data = provider.eth.get_transaction(tx_hash)
    tx_model = TransactionModel(
        txhash=tx_hash.hex(),
        to=tx_data.get("to"),
        value=provider.to_wei(VALUE, "ether")
    )
    return tx_model

def check_sender_balance():
    account: LocalAccount = provider.eth.account.from_key(
        WALLET
    )
    account_balance = provider.eth.get_balance(account.address)
    account_balance_ether = provider.from_wei(account_balance, "ether")
    return account_balance_ether
