from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from core.models import BaseModel
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    """
    Modèle utilisateur personnalisé
    """

    email = models.EmailField(
        unique=True,
        verbose_name="Adresse email",
        help_text="Adresse email unique de l'utilisateur"
    )

    full_name = models.CharField(
        max_length=150,
        verbose_name="Nom complet",
        help_text="Nom et prénom de l'utilisateur"
    )

    is_staff = models.BooleanField(
        default=False,
        verbose_name="Membre du staff",
        help_text="Indique si l'utilisateur peut accéder à l'administration"
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Actif",
        help_text="Indique si le compte est actif"
    )

    date_joined = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date d'inscription"
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"
        ordering = ["-created_at"]

    def __str__(self):
        return self.email
