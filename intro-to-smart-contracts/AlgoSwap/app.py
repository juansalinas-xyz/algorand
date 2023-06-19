from beaker import *
from pyteal import *


class MyState:
    asa_a = GlobalStateValue(
        stack_type=TealType.uint64, default=Int(0), descr="ID del asset A"
    )

    asa_b = GlobalStateValue(
        stack_type=TealType.uint64, default=Int(0), descr="ID del asset B"
    )


app = Application("AlgoSwap", state=MyState)

@app.create(bare=True)
def create() -> Expr:
    return app.initialize_global_state()


@app.external
def opt_into_asset(asset: abi.Asset) -> Expr:
    return Seq(
        If(Txn.sender() == Global.creator_address()).Then(
            Assert(app.state.asa_a == Int(0)),
            app.state.asa_a.set(asset.asset_id())
        ).Else(
            Assert(app.state.asa_b == Int(0)),
            app.state.asa_b.set(asset.asset_id())
        ),
        opt_into_asset_txn(asset.asset_id(), Global.current_application_address())
    )

@app.external
def receive_asset(axfer: abi.AssetTransferTransaction) -> Expr:
    return Seq(
        Assert(axfer.get().asset_receiver() == Global.current_application_address()),
        If(Txn.sender() == Global.creator_address()).Then(
            Assert(axfer.get().xfer_asset() == app.state.asa_a)
        ).Else(
            Assert(axfer.get().xfer_asset() == app.state.asa_b)
        )
    )  

@app.external
def claim_asset(asset: abi.Asset) -> Expr:
    return Seq(
        If(Txn.sender() == Global.creator_address()).Then(
            Assert(app.state.asa_b != Int(0)),
            transfer_asset(app.state.asa_b.get(), Txn.sender())
        ).Else(
            Assert(app.state.asa_a != Int(0)),
            transfer_asset(app.state.asa_a.get(), Txn.sender())
        )        
    )

@Subroutine(TealType.none)
def transfer_asset(asset_id: Expr, asset_receiver: Expr) -> Expr:
    return Seq(
        InnerTxnBuilder.Execute(
            {
                TxnField.type_enum: TxnType.AssetTransfer,
                TxnField.asset_amount: Int(1),
                TxnField.xfer_asset: asset_id,
                TxnField.asset_receiver: asset_receiver,
                TxnField.fee: Int(0),
            }
        )
    ) 


@Subroutine(TealType.none)
def opt_into_asset_txn(asset_id: Expr, asset_receiver: Expr) -> Expr:
    return Seq(
        InnerTxnBuilder.Execute(
            {
                TxnField.type_enum: TxnType.AssetTransfer,
                TxnField.fee: Int(0),
                TxnField.asset_receiver: asset_receiver,
                TxnField.xfer_asset: asset_id,
                TxnField.asset_amount: Int(0),
            }
        )
    )    

if __name__ == "__main__":
    app.build().export("./artifacts")
