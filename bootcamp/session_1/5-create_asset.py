from algosdk import kmd, transaction
from algosdk.wallet import Wallet
from algosdk.v2client import algod

import json
import base64

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
    unsigned_txn = transaction.AssetConfigTxn(sender=addr1,
            sp=params,
            total=10000,  # Fungible tokens tienen un total de emision mayor que 1
            decimals=2,    # Fungible tokens tipicamente tienen decimales mayor que 0
            default_frozen=False,
            unit_name="FUNTOK",
            asset_name="Fun Token",
            manager=addr1,
            strict_empty_address_check=False,
            reserve="",
            freeze="",
            clawback="",
            url="https://path/to/my/fungible/asset/metadata.json",
            metadata_hash="", # Tipicamente incluye el hash de metadata.json (bytes) 
    )

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

    # guardar el asset index en un archivo
    f = open('asset.index', 'w+')
    f.write(f'{confirmed_txn["asset-index"]}')
    f.close()

main()

