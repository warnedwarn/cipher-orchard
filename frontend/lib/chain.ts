'use client';

import { createAccount, createClient } from 'genlayer-js';
import { studionet } from 'genlayer-js/chains';

export const CONTRACT = (process.env.NEXT_PUBLIC_CONTRACT_ADDRESS ||
  '0x06864b30c52Fd1873269E3EE9DF8a62222697555') as `0x${string}`;
export const EXPLORER =
  process.env.NEXT_PUBLIC_EXPLORER_BASE_URL || 'https://explorer-studio.genlayer.com';

const endpoint = 'https://studio.genlayer.com/api';
const reader: any = createClient({ chain: studionet, endpoint, account: createAccount() });
let wallet: any;

export async function connect() {
  const provider: any = (window as any).ethereum;
  if (!provider) throw Error('A browser wallet is required');
  const [account] = await provider.request({ method: 'eth_requestAccounts' });
  if ((await provider.request({ method: 'eth_chainId' })).toLowerCase() !== '0xf22f') {
    await provider.request({
      method: 'wallet_switchEthereumChain',
      params: [{ chainId: '0xf22f' }],
    });
  }
  wallet = createClient({ chain: studionet, endpoint, account, provider });
  return account;
}

export function read(name: string, args: any[] = []) {
  if (!CONTRACT) throw Error('Contract deployment is not configured');
  return reader.readContract({ address: CONTRACT, functionName: name, args });
}

export async function write(name: string, args: any[] = []) {
  if (!wallet) throw Error('Connect a wallet before grafting');
  const hash = await wallet.writeContract({
    address: CONTRACT,
    functionName: name,
    args,
    value: 0n,
  });
  const receipt: any = await wallet.waitForTransactionReceipt({
    hash,
    status: 'FINALIZED',
    retries: 120,
    interval: 5000,
    fullTransaction: true,
  });
  const consensus = String(receipt?.result_name ?? receipt?.resultName ?? '').toUpperCase();
  const rawLeaders =
    receipt?.consensus_data?.leader_receipt ?? receipt?.consensusData?.leaderReceipt ?? [];
  const leaders = Array.isArray(rawLeaders) ? rawLeaders : [rawLeaders];
  const succeeded = leaders.some(
    (row: any) =>
      String(row?.execution_result ?? row?.executionResult ?? '').toUpperCase() === 'SUCCESS',
  );
  if (consensus !== 'MAJORITY_AGREE' || !succeeded) {
    throw Error(`Transaction finalized without successful execution: ${hash}`);
  }
  return hash as string;
}
