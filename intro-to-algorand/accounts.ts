import algosdk from 'algosdk';
import { rl, waitForInput, getTesnetAlgodClient } from './utils';

async function main() {
  // Crear una cuenta:
  const account = algosdk.generateAccount();
  console.log('Address:', account.addr);
  console.log('Mnemonic:', algosdk.secretKeyToMnemonic(account.sk));
  await waitForInput();

  const algodClient = getTesnetAlgodClient()
  let accountInfo = await algodClient.accountInformation(account.addr).do();
  console.log('accountInfo', accountInfo);

  await waitForInput();
}

main().then(() => rl.close());