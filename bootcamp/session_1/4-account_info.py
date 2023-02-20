from algosdk import kmd
from algosdk.wallet import Wallet
from algosdk.v2client import algod
import json

# define los valores de Sandbox para el cliente kmd
kmd_address = "http://localhost:4002"
kmd_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"

#define los valores de Sandbox para el cliente algod
algod_address = "http://localhost:4001"
algod_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"

def main(): 
    # crear el cliente KMD
    kmd_client = kmd.KMDClient(kmd_token, kmd_address)

    # conectar al la wallet default
    wallet = Wallet("unencrypted-default-wallet", "", kmd_client)

    wallet_addresses = wallet.list_keys()

    addr1 = wallet_addresses[0]
    addr2 = wallet_addresses[1]
    addr3 = wallet_addresses[2]

    # crear el cliente algod
    algod_client = algod.AlgodClient(algod_token, algod_address)

    # ver los detalles de las cuentas
    account_info = algod_client.account_info(addr3)
    print("Account information: {}".format(
        json.dumps(account_info, indent=4)))
    account_info = algod_client.account_info(addr2)
    print("Account information: {}".format(
        json.dumps(account_info, indent=4)))
    account_info = algod_client.account_info(addr1)
    print("Account information: {}".format(
        json.dumps(account_info, indent=4)))

main()
