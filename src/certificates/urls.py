from django.urls import path
from . import views

urlpatterns = [
    path("issue/", views.issue_certificate, name="issue_certificate"),
    path("verify/", views.verify_certificate, name="verify_certificate"),
]
