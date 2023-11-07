"""
Custom validations for the user handles.
"""

from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


UserModel = get_user_model()


def custom_validation(data):
    email = data['email'].strip()
    password = data['password'].strip()
    name = data['name'].strip()

    if not email or UserModel.objects.filter(email=email).exists():
        msg = _('Email unavailable.')
        raise ValidationError(msg)
    if not password:
        msg = _('Chosen password is not acceptable.')
        raise ValidationError(msg)
    if not name:
        pass
    return data


def validate_email(data):
    email = data['email'].strip()
    if not email:
        msg = _('An email is required.')
        raise ValidationError(msg)
    return True


def validade_password(data):
    password = data['password'].strip()
    if not password:
        msg = _('A password is required.')
        raise ValidationError(msg)
    return True
