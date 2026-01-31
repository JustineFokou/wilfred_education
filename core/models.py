from django.db import models

# Create your models here.

class BaseModel(models.Model):
    """
    Modèle de base abstrait
    """
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de création"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Date de mise à jour"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Actif",
        help_text="Indique si l'objet est actif ou non"
    )

    class Meta:
        abstract = True
