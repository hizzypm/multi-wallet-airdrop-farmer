#!/usr/bin/env python3
"""Multi-Wallet Airdrop Farmer"""

import argparse
import json
from pathlib import Path
from web3 import Web3
from eth_account import Account
from colorama import Fore, init
from dotenv import load_dotenv
import os

init(autoreset=True)
load_dotenv()

CHAINS = {
    "base": "https://mainnet.base.org",
    "arbitrum": "https://arb1.arbitrum.io/rpc",
    "optimism": "https://mainnet.optimism.io",
}

def load_wallets(keys_dir: Path):
    wallets = []
    for f in keys_dir.glob("*.json"):
        try:
            with open(f) as fp:
                data = json.load(fp)
            pk = data if isinstance(data, str) else data.get("private_key", "")
            if pk.startswith("0x"):
                wallets.append(Account.from_key(pk))
        except Exception:
            pass
    return wallets

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--chain", default="base")
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()
    
    w3 = Web3(Web3.HTTPProvider(CHAINS.get(args.chain, CHAINS["base"])))
    keys_dir = Path(os.getenv("KEYS_DIR", "keys"))
    wallets = load_wallets(keys_dir)
    
    print(f"{Fore.CYAN}Airdrop Farmer - {args.chain}")
    print(f"{Fore.CYAN}Wallets: {len(wallets)}")
    print(f"{Fore.CYAN}Mode: {'EXECUTE' if args.execute else 'DRY-RUN'}\n")
    
    for i, acc in enumerate(wallets, 1):
        balance = w3.from_wei(w3.eth.get_balance(acc.address), "ether")
        print(f"{Fore.GREEN}[{i}] {acc.address[:12]}... | {balance:.4f} ETH")
        
        if args.execute:
            print(f"  {Fore.YELLOW}Would perform airdrop tasks (swap, bridge, etc.)")
    
    print(f"\n{Fore.CYAN}Add specific airdrop tasks in next version.")

if __name__ == "__main__":
    main()
