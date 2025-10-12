from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CertificateIssueForm, CertificateVerifyForm
from .models import Certificate
from .utils import generate_file_hash, send_to_solana


@login_required
def issue_certificate(request):
    """
    Issue/register certificate and record its hash on Solana.
    """
    if request.method == "POST":
        form = CertificateIssueForm(request.POST, request.FILES)
        if form.is_valid():
            certificate_file = form.cleaned_data["certificate_file"]

            # Compute SHA-256 hash
            file_hash = generate_file_hash(certificate_file)

            # Send hash to Solana blockchain
            tx_sig = send_to_solana(file_hash)

            if not tx_sig:
                messages.error(request, "Blockchain transaction failed. Try again.")
                return redirect("issue_certificate")

            # Save certificate in DB
            cert = Certificate.objects.create(
                owner=request.user,
                certificate_file=certificate_file,
                file_hash=file_hash,
                transaction_signature=tx_sig,
                verified=True,
            )

            messages.success(
                request,
                f"Certificate issued successfully! Blockchain Tx: {tx_sig}"
            )
            return redirect("issue_certificate")

    else:
        form = CertificateIssueForm()

    return render(request, "certificates/issue.html", {"form": form})


def verify_certificate(request):
    """
    Verify if a certificate exists and matches the blockchain record.
    """
    verification_result = None
    if request.method == "POST":
        form = CertificateVerifyForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.cleaned_data["certificate_file"]

            # Compute SHA-256 hash of uploaded file
            uploaded_hash = generate_file_hash(uploaded_file)

            # Check database for hash
            try:
                cert = Certificate.objects.get(file_hash=uploaded_hash)
                verification_result = {
                    "status": "valid",
                    "owner": cert.owner.username,
                    "tx": cert.transaction_signature,
                    "issued_at": cert.issued_at,
                }
            except Certificate.DoesNotExist:
                verification_result = {"status": "invalid"}

    else:
        form = CertificateVerifyForm()

    return render(
        request,
        "certificates/verify.html",
        {"form": form, "verification_result": verification_result},
    )
