import algosdk from "algosdk";
import { getTesnetAlgodClient, rl, waitForInput } from './utils';


async function main() {

  const account = algosdk.generateAccount();
  console.log('Address:', account.addr);
  console.log('Mnemonic:', algosdk.secretKeyToMnemonic(account.sk));
  const algodClient = getTesnetAlgodClient();

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

  // Obtener la informacion basica para cada transaccion
  const suggestedParams = await algodClient.getTransactionParams().do();
  console.log('suggestedParams', suggestedParams);

  await waitForInput();
  const dispenserAddress = 'DISPE57MNLYKOMOK3H5IMBAYOYW3YL2CSI6MDOG3RDXSMET35DG4W6SOTI';

  const paymentTxn = algosdk.makePaymentTxnWithSuggestedParamsFromObject({
    suggestedParams,
    from : account.addr,
    to: dispenserAddress,
    amount: 0.5 * 1e6, // * 1e6 para convertir ALGO a microALGO
  });

  const signedPaymentTxn = paymentTxn.signTxn(account.sk);
  await algodClient.sendRawTransaction(signedPaymentTxn).do();
  console.log(`Enviando pago ${paymentTxn.txID()}...`);
  const roundsToWait = 3;

  await algosdk.waitForConfirmation(algodClient, paymentTxn.txID(), roundsToWait);
  console.log(`Transaccion ${paymentTxn.txID()} confirmada! Ver:  https://testnet.algoscan.app/tx/${paymentTxn.txID()}`);

  await waitForInput();

}

main().then(() => rl.close());