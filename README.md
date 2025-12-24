
# Blockchain Document Verification

A Django-based backend application that enables secure certificate management and real-time verification using cryptographic hashing and the Solana blockchain. The system helps prevent certificate forgery by recording immutable certificate fingerprints on-chain and validating uploaded documents against blockchain transaction data.

---

## Overview

Traditional certificate verification methods rely on centralized databases or manual checks, which are prone to tampering and inefficiency. This project introduces a blockchain-backed verification approach where certificates are authenticated by comparing their cryptographic hashes with records stored on the Solana blockchain.

The system supports registering existing certificates without enforcing any predefined format, making it flexible for institutions and organizations with their own certificate designs.

---

## Features

- Secure certificate registration using **SHA-256 hashing**
- On-chain storage of certificate hashes using the **Solana blockchain**
- Real-time certificate verification by recomputing and matching hashes
- Support for externally generated certificates (no fixed template)
- Django-based backend for handling uploads and verification logic
- Dockerized setup for consistent development environment

---

## Tech Stack

- **Backend:** Django, Python  
- **Blockchain:** Solana (Devnet)  
- **Hashing Algorithm:** SHA-256  
- **Database:** PostgreSQL  
- **Blockchain SDK:** solana-py, solders  
- **Containerization:** Docker, Docker Compose  

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/vedant3436/blockchain-certificate-verification.git
   ```

2. Navigate to the project directory:

   ```bash
   cd blockchain-certificate-verification
   ```

3. Build and run the application using Docker:

   ```bash
   docker-compose up --build
   ```

4. Access the application at:

   ```
   http://127.0.0.1:8000/
   ```

---

## Usage

* Upload a certificate document to register it on the blockchain.
* Upload a certificate for verification to check its authenticity against blockchain records.

---

## License

This project is developed for academic and learning purposes.

## Note on Solana Wallet

This project uses a Solana wallet configured for **Devnet** exclusively. The wallet is intended only for development and academic demonstration purposes and does not contain real funds.



