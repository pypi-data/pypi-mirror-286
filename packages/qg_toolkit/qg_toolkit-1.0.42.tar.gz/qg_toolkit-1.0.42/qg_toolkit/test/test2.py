import asyncio

from aptos_sdk.account_address import AccountAddress
from aptos_sdk.async_client import RestClient

# RPC URLs for Aptos Devnet and Mainnet
DEVNET_RPC_URL = "https://aptos.devnet.m1.movementlabs.xyz"

async def get_balance(rpc_url, address):
    client = RestClient(rpc_url)
    account_resource = await client.account_resource(address, "0x1::coin::CoinStore<0x1::aptos_coin::AptosCoin>")
    if account_resource:
        balance = account_resource["data"]["coin"]["value"]
        return int(balance) / 1e8  # converting to APT
    return None

# 账户地址
address = "0x6d06362aadb518f8d24e3cad98668875a980f3cb6e02011c9d0758cfb7a528d9"
loop = asyncio.get_event_loop()
# 获取开发环境余额
devnet_balance = loop.run_until_complete(get_balance(DEVNET_RPC_URL, AccountAddress.from_str(address)))
print(f"Devnet Balance: {devnet_balance} APT")

