import hashlib

def generate_file_hash(file_obj):
    """
    Computes the SHA-256 hash of a given uploaded file.
    Reads the file in chunks to handle large files efficiently.
    """
    sha256 = hashlib.sha256()
    for chunk in file_obj.chunks():
        sha256.update(chunk)
    return sha256.hexdigest()

def send_to_solana(file_hash):
    """Placeholder: sends hash to Solana blockchain and returns transaction signature."""
    print(f"Simulating blockchain transaction for hash: {file_hash}")
    return "mock_tx_signature_123"
