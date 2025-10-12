from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CertificateIssueForm, CertificateVerifyForm
from .models import Certificate
from .utils import generate_file_hash, send_to_solana


@login_required
def issue_certificate(request):
    """
    View to handle certificate issuance/registration.
    """
    if request.method == "POST":
        form = CertificateIssueForm(request.POST, request.FILES)
        if form.is_valid():
            certificate_file = form.cleaned_data["certificate_file"]
            file_hash = generate_file_hash(certificate_file)

            # Save file hash & simulated blockchain record
            tx_sig = send_to_solana(file_hash)

            cert = Certificate.objects.create(
                owner=request.user,
                certificate_file=certificate_file,
                file_hash=file_hash,
                transaction_signature=tx_sig,
                verified=True,  # for now mark true after mock tx
            )

            messages.success(request, f"Certificate issued successfully! Tx: {tx_sig}")
            return redirect("issue_certificate")
    else:
        form = CertificateIssueForm()

    return render(request, "certificates/issue.html", {"form": form})


def verify_certificate(request):
    """
    View to verify if a certificate exists and matches the blockchain record.
    """
    verification_result = None
    if request.method == "POST":
        form = CertificateVerifyForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.cleaned_data["certificate_file"]
            uploaded_hash = generate_file_hash(uploaded_file)

            # Check if hash exists in database (mock for on-chain check)
            try:
                cert = Certificate.objects.get(file_hash=uploaded_hash)
                verification_result = {
                    "status": "valid",
                    "owner": cert.owner.username,
                    "tx": cert.transaction_signature,
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
