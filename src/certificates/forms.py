from django import forms
from .models import Certificate

class CertificateIssueForm(forms.ModelForm):
    """
    Form for issuers to upload or register a certificate.
    """
    class Meta:
        model = Certificate
        fields = ["certificate_file"]
        widgets = {
            "certificate_file": forms.ClearableFileInput(attrs={"class": "form-control"})
        }


class CertificateVerifyForm(forms.Form):
    """
    Form for users to upload a certificate for verification.
    """
    certificate_file = forms.FileField(
        label="Upload Certificate",
        widget=forms.ClearableFileInput(attrs={"class": "form-control"})
    )
