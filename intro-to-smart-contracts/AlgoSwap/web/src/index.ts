import algosdk, { AtomicTransactionComposer } from 'algosdk'
import { PeraSession } from './wallets/pera'
import Utils from './utils'
import * as algokit from '@algorandfoundation/algokit-utils'
import appspec from '../application.json'
import { ApplicationClient } from '@algorandfoundation/algokit-utils/types/app-client'

const pera = new PeraSession()
const algodClient = new algosdk.Algodv2('', 'https://testnet-api.algonode.cloud', '')
const indexerClient = new algosdk.Indexer('', 'https://testnet-idx.algonode.cloud', '')
const contract = new algosdk.ABIContract(appspec.contract)

let swapAppId: number
let swapApp: ApplicationClient

const accountsMenu = document.getElementById('accounts') as HTMLSelectElement
const asaAInput = document.getElementById('asa-a') as HTMLInputElement
const asaBInput = document.getElementById('asa-b') as HTMLInputElement
const buttonIds = ['connect', 'create', 'startA', 'startB', 'claimA', 'claimB']
const buttons: { [key: string]: HTMLButtonElement } = {}

buttonIds.forEach(id => {
  buttons[id] = document.getElementById(id) as HTMLButtonElement
})

async function signer (txns: algosdk.Transaction[]) {
  return await pera.signTxns(txns)
}

buttons.connect.onclick = async () => {
  await pera.getAccounts()
  buttons.create.disabled = false
  pera.accounts.forEach(account => {
    accountsMenu.add(new Option(account, account))
  })
}

buttons.create.onclick = async () => {
  document.getElementById('status').innerHTML = 'Creando app de Swap...'
  const sender = {
    addr: accountsMenu.selectedOptions[0].value,
    signer
  }
  swapApp = algokit.getAppClient(
    {
      app: JSON.stringify(appspec),
      sender,
      creatorAddress: sender.addr,
      indexer: indexerClient,
      id: 0
    },
    algodClient
  )
  const { appId, appAddress, transaction } = await swapApp.create()
  swapAppId = appId
  document.getElementById('status').innerHTML = `App creada con id ${appId} y address ${appAddress} con tx ${transaction.txID()}. <a href='https://testnet.algoscan.app/app/${appId}'>Ver</a>`
  buttons.startA.disabled = false
  buttons.create.disabled = true
}

buttons.startA.onclick = async () => {
  document.getElementById('status').innerHTML = 'Enviando asset A ...'
  const sender = accountsMenu.selectedOptions[0].value
  const atc = new algosdk.AtomicTransactionComposer()
  const asa = asaAInput.valueAsNumber
  const suggestedParams = await algodClient.getTransactionParams().do()
  // Fondear app
  const payment = algosdk.makePaymentTxnWithSuggestedParamsFromObject({
    suggestedParams,
    amount: 300_000,
    from: sender,
    to: algosdk.getApplicationAddress(swapAppId)
  })
  atc.addTransaction({ txn: payment, signer })
 
  atc.addMethodCall(
    {
      appID: swapAppId,
      method: algosdk.getMethodByName(contract.methods, 'opt_into_asset'),
      sender,
      signer,
      suggestedParams: { ...suggestedParams, fee: 2_000, flatFee: true },
      methodArgs: [asa]
    })

  const axfer = algosdk.makeAssetTransferTxnWithSuggestedParamsFromObject({
    suggestedParams,
    from: sender,
    amount: 1,
    to: algosdk.getApplicationAddress(swapAppId),
    assetIndex: asa
  })

  atc.addMethodCall(
    {
      appID: swapAppId,
      method: algosdk.getMethodByName(contract.methods, 'receive_asset'),
      sender,
      signer,
      suggestedParams: await algodClient.getTransactionParams().do(),
      methodArgs: [{ txn: axfer, signer }]
    })

  await atc.execute(algodClient, 3)
  document.getElementById('status').innerHTML = `Asset recibido! <a href='https://testnet.algoscan.app/app/${swapAppId}'>Ver</a>`
  buttons.startA.disabled = true
  buttons.startB.disabled = false
}

buttons.startB.onclick = async () => {

  document.getElementById('status').innerHTML = 'Iniciando Swap ...'
  const sender = accountsMenu.selectedOptions[0].value
  const atc = new algosdk.AtomicTransactionComposer()
  const asaB = asaBInput.valueAsNumber
  const suggestedParams = await algodClient.getTransactionParams().do()

  atc.addMethodCall(
    {
      appID: swapAppId,
      method: algosdk.getMethodByName(contract.methods, 'opt_into_asset'),
      sender,
      signer,
      suggestedParams: { ...suggestedParams, fee: 2_000, flatFee: true },
      methodArgs: [asaB]
    })

  const axfer = algosdk.makeAssetTransferTxnWithSuggestedParamsFromObject({
    suggestedParams,
    from: sender,
    amount: 1,
    to: algosdk.getApplicationAddress(swapAppId),
    assetIndex: asaB
  })

  atc.addMethodCall(
    {
      appID: swapAppId,
      method: algosdk.getMethodByName(contract.methods, 'receive_asset'),
      sender,
      signer,
      suggestedParams: { ...suggestedParams, fee: 2_000, flatFee: true },
      methodArgs: [{ txn: axfer, signer }]
    })

  
  const state = (await algodClient.getApplicationByID(swapAppId).do()).params['global-state']
  const readableState = Utils.getReadableState(state)
  const asaA = readableState.asa_a.number
  
  const optInTxn = algosdk.makeAssetTransferTxnWithSuggestedParamsFromObject({
      from: sender,
      to: sender,
      suggestedParams,
      assetIndex: asaA,
      amount: 0,
    });
  
  atc.addTransaction({ txn: optInTxn, signer })
  
  atc.addMethodCall(
    {
      appID: swapAppId,
      method: algosdk.getMethodByName(contract.methods, 'claim_asset'),
      sender,
      signer,
      suggestedParams: { ...suggestedParams, fee: 2_000, flatFee: true },
      methodArgs: [asaA],
    }
  )

  await atc.execute(algodClient, 3)
  document.getElementById('status').innerHTML = `Asset enviado! <a href='https://testnet.algoscan.app/app/${swapAppId}'>Ver</a>`
  buttons.startB.disabled = true
  buttons.claimB.disabled = false
}

buttons.claimB.onclick = async () => {

  document.getElementById('status').innerHTML = 'Reclamando asset B ...'
  const sender = accountsMenu.selectedOptions[0].value
  const atc = new algosdk.AtomicTransactionComposer()
  const suggestedParams = await algodClient.getTransactionParams().do()

  const state = (await algodClient.getApplicationByID(swapAppId).do()).params['global-state']
  const readableState = Utils.getReadableState(state)
  const asaB = readableState.asa_b.number

  const optInTxn = algosdk.makeAssetTransferTxnWithSuggestedParamsFromObject({
    from: sender,
    to: sender,
    suggestedParams,
    assetIndex: asaB,
    amount: 0,
  });

  atc.addTransaction({ txn: optInTxn, signer })

  atc.addMethodCall(
    {
      appID: swapAppId,
      method: algosdk.getMethodByName(contract.methods, 'claim_asset'),
      sender,
      signer,
      suggestedParams: { ...suggestedParams, fee: 2_000, flatFee: true },
      methodArgs: [asaB],
    }
  )

  await atc.execute(algodClient, 3)
  document.getElementById('status').innerHTML = `Asset enviado! <a href='https://testnet.algoscan.app/app/${swapAppId}'>Ver</a>`
  buttons.claimB.disabled = true
}
