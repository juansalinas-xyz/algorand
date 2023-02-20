from algosdk import kmd, transaction
from algosdk.wallet import Wallet
from algosdk.v2client import algod

import json
import base64

# define sandbox values for kmd client
kmd_address = "http://localhost:4002"
kmd_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    
# define sandbox values for algod client
algod_address = "http://localhost:4001"
algod_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"

def get_asset_index(default_index = 3): 
    # tratar de leer el index del asset desde el entorno de archivos
    try: 
        index = int(open('asset.index', 'r')).readLine()
    # sino retorna el default index
    except: 
        index = default_index
    return index



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
    sender = addr2
    index = get_asset_index(default_index=3)
    unsigned_txn = transaction.AssetOptInTxn(sender, params, index)

    # firmar la transacción
    signed_txn = unsigned_txn.sign(wallet.export_key(addr2))

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

main()

