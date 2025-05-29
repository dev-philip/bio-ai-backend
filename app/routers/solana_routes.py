import json
from fastapi import APIRouter, HTTPException
from solana.rpc.async_api import AsyncClient 
from solders.keypair import Keypair  
from solders.pubkey import Pubkey as PublicKey
from solders.transaction import Transaction
from solders.system_program import transfer, TransferParams
from solana.rpc.types import TxOpts
import base58
import asyncio

router = APIRouter()

# Async Solana client
solana_client = AsyncClient("https://api.devnet.solana.com")

# Load keypair
def load_keypair(path):
    with open(path) as f:
        return Keypair.from_bytes(bytes(json.load(f)))

# Get public key
grab_key = load_keypair("app/keys/my-keypair.json")
signer = grab_key.pubkey()


@router.post("/send-to-solana")
async def send_to_solana():
    # Placeholder PublicKeys - replace with actual Devnet public keys
    # For testing, you can use a Phantom wallet's Devnet address
    # Make sure 'YourProgramPublicKey' is indeed a program ID if you're interacting with one.
    # If it's a regular account, rename it accordingly.
    # Example: receiver_account = PublicKey("GdK5sT8MhS353P1w2fA2Kk8Y5Q3uG2b9R4xW5fV6g2j")
    program_id = PublicKey("YourProgramPublicKey") # This might not be needed for a simple SOL transfer
    receiver_account = PublicKey("TargetAccountPublicKey")

    # It's important to use the signer's actual public key (pubkey() method)
    instruction = transfer(
        TransferParams(
            from_pubkey=signer.pubkey(), # Use signer.pubkey()
            to_pubkey=receiver_account,
            lamports=1_000_000  # 0.001 SOL
        )
    )

    tx = Transaction().add(instruction)

    try:
        # Use await for asynchronous calls
        # Pass the signer as a list
        response = await async_solana_client.send_transaction(tx, signer, opts=TxOpts(skip_preflight=True, skip_confirmation=False))
        # It's good practice to wait for confirmation
        await async_solana_client.confirm_transaction(response.value)
        return {"tx_signature": response.value}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error sending transaction: {e}")

@router.get("/account/{account_pubkey}")
async def get_account(account_pubkey: str):
    try:
        # Validate public key format
        decoded = base58.b58decode(account_pubkey)
        if len(decoded) != 32:
            raise ValueError("Decoded key is not 32 bytes.")
        pubkey_obj = PublicKey.from_bytes(decoded)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid public key format: {e}")

    try:
        # Fetch account info
        resp = await solana_client.get_account_info(pubkey_obj)

        if not resp.value:
            raise HTTPException(status_code=404, detail="Account not found.")

        # Handle empty or no data gracefully
        try:
            if not resp.value.data or not resp.value.data[0]:
                raw_data = b""
                data_base64 = ""
            else:
                data_base64 = resp.value.data[0]
                raw_data = base64.b64decode(data_base64)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error decoding account data: {e}")

        # Try to decode to text
        try:
            decoded_text = raw_data.decode("utf-8")
        except UnicodeDecodeError:
            decoded_text = None

        return {
            "base64": data_base64,
            "raw_bytes": list(raw_data),
            "decoded_text": decoded_text,
            "owner": str(resp.value.owner),
            "executable": resp.value.executable,
            "lamports": resp.value.lamports,
        }

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching account info: {e}")