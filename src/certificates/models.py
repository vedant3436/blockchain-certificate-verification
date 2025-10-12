from django.db import models
from django.conf import settings

class Certificate(models.Model):
    """
    Represents a digital or uploaded certificate that has been issued or registered.
    """
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='certificates',
        help_text="User to whom the certificate belongs."
    )
    certificate_file = models.FileField(upload_to="certificates/")
    file_hash = models.CharField(max_length=256, unique=True)
    transaction_signature = models.CharField(max_length=128, blank=True, null=True)
    issued_at = models.DateTimeField(auto_now_add=True)
    verified = models.BooleanField(default=False)
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Certificate - {self.owner.username} ({self.file_hash[:10]}...)"
