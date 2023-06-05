import algosdk from "algosdk";
import { getTesnetAlgodClient, waitForInput, rl } from './utils';

// Fondeando wallet con el ALGO dispenser en la tesnet de Algorand
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
  await waitForInput();

}

main().then(() => rl.close());