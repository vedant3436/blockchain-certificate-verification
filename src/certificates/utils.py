import os
import json
import time
import hashlib
from solana.rpc.api import Client
from solana.publickey import PublicKey
from solana.keypair import Keypair
from solana.transaction import Transaction, TransactionInstruction
from solana.rpc.types import TxOpts
from solders.signature import Signature
from solders.hash import Hash


SOLANA_RPC_URL = os.getenv("SOLANA_RPC_URL", "https://api.devnet.solana.com")
KEYPAIR_PATH = os.getenv("SOLANA_KEYPAIR_PATH")

client = Client(SOLANA_RPC_URL)
MEMO_PROGRAM_ID = PublicKey("MemoSq4gqABAXKb96qnH8TysNcWxMyWCqXgDLGmfcHr")


def generate_file_hash(file_obj):
    """
    Compute SHA-256 hash of uploaded file.
    """
    sha256 = hashlib.sha256()
    for chunk in file_obj.chunks():
        sha256.update(chunk)
    return sha256.hexdigest()


def load_keypair():
    """
    Loads Solana wallet keypair from JSON file (64 integers)
    """
    with open(KEYPAIR_PATH, "r") as f:
        secret_list = json.load(f)
    secret_bytes = bytes(secret_list)
    return Keypair.from_secret_key(secret_bytes)


# Ensure sufficient balance
def ensure_balance(keypair: Keypair, min_lamports: int = 100_000_000): #change int to 50k to 1000k as per need
    lamports = client.get_balance(keypair.public_key).value

    while lamports < min_lamports:
        airdrop_amount = 100000000 #min(100_000, min_lamports - lamports)   max safe per Devnet airdrop
        print(f"Airdropping {airdrop_amount} lamports to {keypair.public_key}...")
        client.request_airdrop(keypair.public_key, airdrop_amount)

        # Wait for balance to update
        for _ in range(15):
            time.sleep(1)
            lamports = client.get_balance(keypair.public_key).value
            if lamports >= min_lamports:
                print(f"Airdrop confirmed. Current balance: {lamports}")
                break
        else:
            print(f"Airdrop may not have confirmed yet. Current balance: {lamports}")
            break

    print(f"Wallet has sufficient balance: {lamports} lamports.")


def send_to_solana(file_hash: str, min_lamports: int = 100_000_000): #change int to 50k to 1000k as per need
    """
    Sends a certificate hash to Solana Devnet via Memo program.
    Returns the transaction signature (base58 string) on success, None on failure.
    """
    try:
        keypair = load_keypair()
        ensure_balance(keypair, min_lamports=min_lamports)

        hash_data = file_hash.encode("utf-8")

        # Memo program instruction
        instruction = TransactionInstruction(
            keys=[],  # Memo program doesn't require accounts
            program_id=MEMO_PROGRAM_ID,
            data=hash_data
        )

        # Build transaction
        txn = Transaction()
        txn.add(instruction)
        txn.fee_payer = keypair.public_key

        # Latest blockhash
        latest_blockhash_resp = client.get_latest_blockhash(commitment="confirmed")
        blockhash_obj = latest_blockhash_resp.value.blockhash
        txn.recent_blockhash = str(blockhash_obj)

        # Sign transaction
        txn.sign(keypair)
        raw_tx = txn.serialize()

        # Send raw transaction
        response = client.send_raw_transaction(
            raw_tx,
            opts=TxOpts(skip_preflight=False, preflight_commitment="confirmed")
        )

        # Extract signature
        tx_sig = getattr(response, "result", None)
        if tx_sig:
            tx_sig = str(tx_sig)
        else:
            # fallback: use the signed transaction's signature directly
            if txn.signatures:
                tx_sig = str(txn.signatures[0])
            else:
                tx_sig = None

        if tx_sig:
            print(f"Transaction successful: {tx_sig}")
            return tx_sig

        print("Transaction failed: no signature returned.")
        return None

    except Exception as e:
        print(f"Transaction failed: {e}")
        return None
