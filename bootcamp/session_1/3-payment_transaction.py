from algosdk import transaction
import json
import base64

from algosdk import kmd
from algosdk.wallet import Wallet
from algosdk.v2client import algod

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

    # build una transacción sin firma
    params = algod_client.suggested_params()
    receiver = addr2
    note = "Hello word".encode()
    amount = 1000000
    unsigned_txn = transaction.PaymentTxn(addr1, params, receiver, amount, None, note)

    # firmar la transacción
    signed_txn = unsigned_txn.sign(wallet.export_key(addr1))

    # enviar la transacción
    txid = algod_client.send_transaction(signed_txn)
    print("Successfully sent transaction with txID: {}".format(txid))

    # esperar por la confirmación: 

    try: 
        confirmed_txn = transaction.wait_for_confirmation(algod_client, txid, 4)
    except Exception as err: 
        print(err)
        return
    
    print("Transaction information: {}".format(
        json.dumps(confirmed_txn, indent=4)))
    print("Decoded note: {}".format(base64.b64decode(
        confirmed_txn["txn"]["txn"]["note"]).decode()))

main()
