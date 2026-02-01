from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from core.models import BaseModel 


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("role", "admin")
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    """
    Custom User model
    """

    ROLE_ADMIN = "admin"
    ROLE_STAFF = "staff"
    ROLE_ENSEIGNANT = "enseignant"
    ROLE_ETUDIANT = "etudiant"
    ROLE_CHOICES = [
        (ROLE_ADMIN, "Admin"),
        (ROLE_STAFF, "Staff"),
        (ROLE_ENSEIGNANT, "Enseignant"),
        (ROLE_ETUDIANT, "Étudiant"),
    ]

    email = models.EmailField(
        unique=True,
        verbose_name="Email address"
    )

    first_name = models.CharField(
        max_length=100,
        verbose_name="First name"
    )

    last_name = models.CharField(
        max_length=100,
        verbose_name="Last name"
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Phone number"
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=ROLE_ETUDIANT,
        verbose_name="Rôle"
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.email

    def get_full_name(self):
        return self.full_name

    @property
    def role_color(self):
        colors = {
            self.ROLE_ADMIN: "blue",
            self.ROLE_STAFF: "amber",
            self.ROLE_ENSEIGNANT: "green",
            self.ROLE_ETUDIANT: "purple",
        }
        return colors.get(self.role, "blue")