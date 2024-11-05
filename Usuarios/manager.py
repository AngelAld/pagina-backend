from multiprocessing.pool import IMapIterator
from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def email_validator(self, email):
        try:
            validate_email(email)
        except ValidationError:
            raise ValidationError(_("El correo electrónico no es válido"))

    def create_user(self, email, nombres, apellidos, password, **extra_fields):
        if not email:
            raise ValueError(_("El correo electrónico es obligatorio"))
        if not nombres:
            raise ValueError(_("Los nombres son obligatorios"))
        if not apellidos:
            raise ValueError(_("Los apellidos son obligatorios"))
        self.email_validator(email)
        email = self.normalize_email(email)
        user = self.model(
            email=email, nombres=nombres, apellidos=apellidos, **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nombres, apellidos, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_verified", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("El superusuario debe tener is_staff=True"))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("El superusuario debe tener is_superuser=True"))
        if extra_fields.get("is_verified") is not True:
            raise ValueError(_("El superusuario debe tener is_verified=True"))

        return self.create_user(email, nombres, apellidos, password, **extra_fields)
