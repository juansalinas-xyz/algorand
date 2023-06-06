import algosdk from 'algosdk';
import { waitForInput, getTesnetAlgodClient, rl } from './utils';

async function main() {

  // Las cuentas en Algorand no "se crean" en si, en realidad son el resultado de un proceso de hashing y concatenacion de llaves, por ende, todas las cuentas posibles en algorand no existen en la red, sino son el resultado de este algoritmo. 
  // Para "existir" en cierto modo, deben estar activas, y para esto deben tener un balance mínimo de 0.1 ALGO  
  // Ver a detalle: https://developer.algorand.org/docs/get-details/accounts/
  const account = algosdk.generateAccount();
  console.log('Address:', account.addr);
  console.log('Mnemonic:', algosdk.secretKeyToMnemonic(account.sk));
  const algodClient = getTesnetAlgodClient()

  console.log('Enviar ALGO desde https://testnet.algoexplorer.io/dispenser. El programa continuara una vez que se reciba ALGO...');

  let accountInfo = await algodClient.accountInformation(account.addr).do();

  const waitForBalance = async () => {
    accountInfo = await algodClient.accountInformation(account.addr).do();
    const balance = accountInfo.amount;
    if (balance === 0) {
      await waitForBalance();
    }
  }

  await waitForBalance();
  console.log(`${account.addr} fondeada!`);
  await waitForInput();

  const suggestedParams = await algodClient.getTransactionParams().do();
  
  const assetCreateTxn = algosdk.makeAssetCreateTxnWithSuggestedParamsFromObject({
    suggestedParams,
    from: account.addr, // La cuenta que creará el asset.
    assetName: 'My First Asset', // El nombre del asset
    unitName: 'MFA', // El nombre corto del asset
    total: 100, // El total de la unidad más pequeña del activo
    decimals: 1, // El numero de decimales en el asset
    reserve: account.addr, // La dirección de la cuenta que contiene el suministro sin circular/sin acuñar del activo
    freeze: account.addr, // La dirección de la cuenta que puede congelar o descongelar el activo en una cuenta específica
    defaultFrozen: false, // Si el activo está o no congelado por defecto
    clawback: account.addr, // La dirección de la cuenta que puede recuperar el activo
    assetURL: 'https://developer.algorand.org', // La URL donde se puede recuperar más información sobre el asset
    manager: account.addr, // La dirección de la cuenta que puede cambiar las direcciones de reserva, congelación, recuperación y administrador
  });

  const signedAssetCreateTxn = assetCreateTxn.signTxn(account.sk);

  await algodClient.sendRawTransaction(signedAssetCreateTxn).do();
  console.log(`Enviando transaccion de creacion de asset ${assetCreateTxn.txID()}...`);
  const roundsToWait = 3;
  await algosdk.waitForConfirmation(algodClient, assetCreateTxn.txID(), roundsToWait);

  const assetCreateInfo = await algodClient
    .pendingTransactionInformation(assetCreateTxn.txID()).do();

  const assetIndex = assetCreateInfo['asset-index'];

  console.log(`Asset ${assetIndex} creado! Ver la transaccion en https://testnet.algoscan.app/tx/${assetCreateTxn.txID()}`);

  await waitForInput();

  // Transfer asset
  const newAccount = algosdk.generateAccount();

  const assetTransferTxn = algosdk.makeAssetTransferTxnWithSuggestedParamsFromObject({
    suggestedParams,
    from: account.addr,
    to: newAccount.addr,
    amount: 25,
    assetIndex,
  });

  const signedAssetTransferTxn = assetTransferTxn.signTxn(account.sk);

  try {
    console.log('Transfiriendo asset a ', newAccount.addr);
    await algodClient.sendRawTransaction(signedAssetTransferTxn).do();
  } catch (e) {
    console.log('ERROR', e.response.body.message);
  }

  await waitForInput();

  // Usar una atomic transaction group para transferir el asset con exito
  // Fondear la nueva cuenta
  // La cuenta necesita 0.2 ALGO para recibir un Asset
  // 0.1 ALGO es la cantidad minima de ALGO que se necesita para que la cuenta sea activada o agregada a la blockchain, 
  // ver a detalle: https://developer.algorand.org/docs/get-details/accounts/
  // Adicionalmente se necesitan 0.1 ALGO (Opt-in) por cada asset que una cuenta tiene almacenada, para rentar el espacio en la blockchain.
  const fundTxn = algosdk.makePaymentTxnWithSuggestedParamsFromObject({
    from: account.addr,
    to: newAccount.addr,
    amount: 200_000, // 0.2 ALGO,
    // Doblamos el fee, entonces newAccount no necesita pagar un fee
    suggestedParams: { ...suggestedParams, fee: 2 * algosdk.ALGORAND_MIN_TX_FEE, flatFee: true },
  });
  
  // Opt-in: 0 para la transferencia del asset, es una transferencia a si mismo
  const optInTxn = algosdk.makeAssetTransferTxnWithSuggestedParamsFromObject({
    from: newAccount.addr,
    to: newAccount.addr,
    amount: 0,
    assetIndex,
    // Set fee to zero since account will be paying double fee
    suggestedParams: { ...suggestedParams, fee: 0, flatFee: true },
  });

  const txns = [fundTxn, optInTxn, assetTransferTxn];
  const txnGroup = algosdk.assignGroupID(txns);
  const signedTxns = [
    txnGroup[0].signTxn(account.sk),
    txnGroup[1].signTxn(newAccount.sk),
    txnGroup[2].signTxn(account.sk),
  ];

  const groupID = txnGroup[0].group!;
  const encodedGroupID = groupID.toString('base64');
  console.log(`Eviando atomic transaction group ${encodedGroupID}...`);
  await algodClient.sendRawTransaction(signedTxns).do();
  await algosdk.waitForConfirmation(algodClient, txnGroup[0].txID(), roundsToWait);

  console.log(`Transacciones confirmadas! Ver en https://testnet.algoscan.app/tx/group/${encodeURIComponent(encodedGroupID)}`);

  await waitForInput();

}

main().then(() => rl.close());