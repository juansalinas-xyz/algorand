import readline from 'readline';
import algosdk from 'algosdk';

export const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
const skipPrompts = process.argv.includes('--skip-prompts');

export function waitForInput() {
    if (skipPrompts === true) return new Promise((resolve) => { resolve(true); });
    return new Promise((resolve) => {
      rl.question('Presiona enter para continuar...', resolve);
    });
  }

  export function getLocalAlgodClient() {
    const algodToken = 'a'.repeat(64);
    const algodServer = 'http://localhost';
    const algodPort = process.env.ALGOD_PORT || '4001';
  
    const algodClient = new algosdk.Algodv2(algodToken, algodServer, algodPort);
    return algodClient;
  }

  export function getTesnetAlgodClient() {
    const algodToken = '';
    const algodServer = 'https://testnet-api.algonode.cloud';
    const algodPort = undefined;
    const algodClient = new algosdk.Algodv2(algodToken, algodServer, algodPort);
    return algodClient;
  }