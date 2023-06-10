from typing import Final 

from beaker import *
from pyteal import *


class AuctionState:
    highest_bidder: Final[GlobalStateValue] = GlobalStateValue(
        stack_type=TealType.bytes,
        default=Bytes(""),
        descr="Address del apostador mayor"
    )

    auction_end: Final[GlobalStateValue] = GlobalStateValue(
        stack_type=TealType.uint64,
        default=Int(0),
        descr="Timestamp de finalizacion de la subasta"
    )

    highest_bid : Final[GlobalStateValue] = GlobalStateValue(
        stack_type=TealType.uint64,
        default=Int(0),
        descr="Cantidad de las oferta mayor (uALGO)"
    )

    asa_amt: Final[GlobalStateValue] = GlobalStateValue(
        stack_type=TealType.uint64,
        default=Int(0),
        descr="Cantidad total del ASA a subastar"
    )

    asa: Final[GlobalStateValue] = GlobalStateValue(
        stack_type=TealType.uint64,
        default=Int(0),
        descr="El ID del ASA a subastar"
    )

app = Application("Auction", state=AuctionState)

@app.create(bare=True)
def create() -> Expr: 
    # Setea todos los valores de global state por default
    return app.initialize_global_state()

@app.external(authorize=Authorize.only(Global.creator_address()))
def opt_into_asset(asset: abi.Asset) -> Expr:
    return Seq(
        # Verificar que ya no se haya hecho opt-in sobre el ASA
        Assert(app.state.asa == Int(0)),
        # Guardar el ID del ASA en el global state
        app.state.asa.set(asset.asset_id()),
        # Enviar transaccion de opt-in, transferencia de 0 asset a si mismo
        InnerTxnBuilder.Execute(
            {
                TxnField.type_enum: TxnType.AssetTransfer,
                TxnField.fee: Int(0), # el fee se cubre con la txn exterior
                TxnField.asset_receiver : Global.current_application_address(),
                TxnField.xfer_asset: asset.asset_id(),
                TxnField.asset_amount: Int(0)
            }
        )
    )

@app.external(authorize=Authorize.only(Global.creator_address()))
def start_auction(
    starting_price: abi.Uint64,
    length: abi.Uint64,
    axfer: abi.AssetTransferTransaction
) -> Expr: 
    return Seq(
        # Nos aseguramos que la subasta no haya sido iniciada
        Assert(app.state.auction_end.get() == Int(0)),
        Assert(axfer.get().asset_receiver() == Global.current_application_address()),
        Assert(axfer.get().xfer_asset() == app.state.asa),
        # Seteamos el global state
        app.state.asa_amt.set(axfer.get().asset_amount()),
        app.state.auction_end.set(Global.latest_timestamp() + length.get()),
        app.state.highest_bid.set(starting_price.get())
    )

@Subroutine(TealType.none)
def pay(recreiver: Expr, amount: Expr) -> Expr: 
    return InnerTxnBuilder.Execute(
        {
            TxnField.type_enum: TxnType.Payment,
            TxnField.receiver: recreiver,
            TxnField.amount: amount,
            TxnField.fee: Int(0)
        }
    )

@app.external
def bid(
    payment: abi.PaymentTransaction,
    previous_bidder: abi.Account
) -> Expr: 
    return Seq(
        # Nos aseguramos que no haya terminado la subasta
        Assert(Global.latest_timestamp() < app.state.auction_end.get()),
        # Verificar la transaccion de pago
        Assert(payment.get().amount() > app.state.highest_bid.get()),
        Assert(Txn.sender() == payment.get().sender()),
        Assert(payment.get().receiver() == Global.current_application_address()),
        # Se retorna la oferta previa mas alta, si hubo alguna
        If(
            app.state.highest_bidder.get() != Bytes(""),
            pay(app.state.highest_bidder.get(), app.state.highest_bid.get()),
        ),
        # Setear el global state
        app.state.highest_bid.set(payment.get().amount()),
        app.state.highest_bidder.set(payment.get().sender())
    )

@app.external
def claim_asset(
    asset: abi.Asset,
    asset_creator: abi.Account
) -> Expr : 
    return Seq(
        # Se verifica que la subasta haya terminado
        Assert(Global.latest_timestamp() > app.state.auction_end.get()),
        InnerTxnBuilder.Execute(
            {
                TxnField.type_enum: TxnType.AssetTransfer,
                TxnField.fee: Int(0), # cubierto con el fee de la txn externa
                TxnField.xfer_asset: app.state.asa,
                TxnField.asset_amount: app.state.asa_amt,
                TxnField.asset_receiver: app.state.highest_bidder,
                TxnField.asset_close_to: asset_creator.address()
            }
        )
    )

@app.delete
def delete() -> Expr: 
    return InnerTxnBuilder.Execute(
        {
          TxnField.type_enum: TxnType.Payment,
          TxnField.fee: Int(0),
          TxnField.receiver: Global.creator_address(),
          # Se envia todo el balance al creador, incluso el 0.1 minimo requerido
          TxnField.close_remainder_to: Global.creator_address(),
          # Se cierra la cuenta, entonces el importe se setea en cero
          TxnField.amount: Int(0)  
        }
    )         
    

if __name__ == "__main__":
    app.build().export("./artifacts")
