from beaker import *
from pyteal import *


class MyState:
    highest_bidder = GlobalStateValue(
        stack_type=TealType.bytes, default=Bytes(""), descr="Apostador mayor"
    )

    highest_bid = GlobalStateValue(
        stack_type=TealType.uint64, default=Int(0), descr="Apuesta mayor"
    )

    auction_end = GlobalStateValue(
        stack_type=TealType.uint64,
        default=Int(0),
        descr="Timestamp del final de la subasta",
    )

    asa_id = GlobalStateValue(
        stack_type=TealType.uint64, default=Int(0), descr="ID del asset a subastar"
    )


app = Application("AuctionApp", state=MyState)

@app.create(bare=True)
def create() -> Expr:
    # Setea todos los valores de global state por default
    return app.initialize_global_state()


@app.external(authorize=Authorize.only(Global.creator_address()))
def opt_into_asset(asset: abi.Asset) -> Expr:
    return Seq(
        # Verificar que ya no se haya hecho opt-in sobre el ASA
        Assert(app.state.asa_id == Int(0)),
        # Guardar el ID del ASA en el global state
        app.state.asa_id.set(asset.asset_id()),
        # Enviar transaccion de opt-in, transferencia de 0 asset a si mismo
        InnerTxnBuilder.Execute(
            {
                TxnField.type_enum: TxnType.AssetTransfer,
                TxnField.fee: Int(0),  # el fee se cubre con la txn exterior
                TxnField.asset_receiver: Global.current_application_address(),
                TxnField.xfer_asset: asset.asset_id(),
                TxnField.asset_amount: Int(0),
            }
        ),
    )


@app.external(authorize=Authorize.only(Global.creator_address()))
def start_auction(
    starting_price: abi.Uint64, length: abi.Uint64, axfer: abi.AssetTransferTransaction
) -> Expr:
    return Seq(
        If(app.state.auction_end.get() == Int(0)).Then(
            Assert(axfer.get().asset_receiver() == Global.current_application_address()),
            Assert(axfer.get().xfer_asset() == app.state.asa_id.get()),
            app.state.highest_bid.set(starting_price.get()),
            app.state.auction_end.set(Global.latest_timestamp() + length.get()),
            app.state.asa_id.set(axfer.get().xfer_asset())
        ).Else(
            If(Global.latest_timestamp() >= app.state.auction_end.get()).Then(
                app.state.highest_bid.set(starting_price.get()),
                app.state.highest_bidder.set(Bytes("")),
                app.state.auction_end.set(Global.latest_timestamp() + length.get()),
                app.state.asa_id.set(axfer.get().xfer_asset())
            ).Else(
                Assert(Global.latest_timestamp() >= app.state.auction_end.get()
                , comment="NOT_ENDED")
            )
        )
    )


@Subroutine(TealType.none)
def pay(recreiver: Expr, amount: Expr) -> Expr:
    return InnerTxnBuilder.Execute(
        {
            TxnField.type_enum: TxnType.Payment,
            TxnField.receiver: recreiver,
            TxnField.amount: amount,
            TxnField.fee: Int(0),
        }
    )


@app.external
def bid(payment: abi.PaymentTransaction, previous_bidder: abi.Account) -> Expr:
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
        app.state.highest_bidder.set(payment.get().sender()),
    )


@app.external
def claim_asset(asset: abi.Asset) -> Expr:
    return Seq(
        Assert(Global.latest_timestamp() >= app.state.auction_end.get()),
        Assert(Txn.sender() == app.state.highest_bidder.get()),
        # Transaccion interna de envío de asset
        InnerTxnBuilder.Execute(
            {
                TxnField.type_enum: TxnType.AssetTransfer,
                TxnField.asset_amount: Int(1),
                TxnField.xfer_asset: app.state.asa_id.get(),
                TxnField.asset_receiver: app.state.highest_bidder.get(),
                TxnField.fee: Int(0),
            }
        ),
    )


@app.external(authorize=Authorize.only(Global.creator_address()))
def claim_asset_without_bids(asset: abi.Asset) -> Expr:
    return Seq(
        Assert(Global.latest_timestamp() >= app.state.auction_end.get()),
        Assert(app.state.highest_bidder.get() == Bytes("")),
        # Transaccion interna de envío de asset
        InnerTxnBuilder.Execute(
            {
                TxnField.type_enum: TxnType.AssetTransfer,
                TxnField.asset_amount: Int(1),
                TxnField.xfer_asset: app.state.asa_id.get(),
                TxnField.asset_receiver: Global.creator_address(),
                TxnField.fee: Int(0),
            }
        ),
    )


@app.external(authorize=Authorize.only(Global.creator_address()))
def claim_bid() -> Expr:
    return Seq(
        Assert(Global.latest_timestamp() >= app.state.auction_end.get()),
        pay(Global.creator_address(), app.state.highest_bid.get()),
    )


if __name__ == "__main__":
    app.build().export("./artifacts")
