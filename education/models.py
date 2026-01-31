from django.db import models
from core.models import BaseModel

# Create your models here.
class Level(BaseModel):
    """
    Modèle pour les niveaux scolaires
    """
    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Nom du niveau",
        help_text="Ex: Primaire, Secondaire, Supérieur"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Description",
        help_text="Description du niveau"
    )

    class Meta:
        verbose_name = "Niveau"
        verbose_name_plural = "Niveaux"
        ordering = ['id']

    def __str__(self):
        return self.name



class ClassLevel(BaseModel):
    """
    Modèle pour les classes scolaires
    """
    level = models.ForeignKey(
        Level,
        on_delete=models.CASCADE,
        related_name="classes",
        verbose_name="Niveau",
        help_text="Niveau scolaire associé"
    )
    name = models.CharField(
        max_length=50,
        verbose_name="Nom de la classe",
        help_text="Ex: CP, CE1, 6e, Terminale, L1"
    )

    class Meta:
        verbose_name = "Classe"
        verbose_name_plural = "Classes"
        ordering = ['id']
        unique_together = ('level', 'name')

    def __str__(self):
        return f"{self.name} ({self.level.name})"


class Subject(BaseModel):
    """
    Modèle pour les matières
    """
    class_level = models.ForeignKey(
        ClassLevel,
        on_delete=models.CASCADE,
        related_name="subjects",
        verbose_name="Classe",
        help_text="Classe associée"
    )
    name = models.CharField(
        max_length=100,
        verbose_name="Nom de la matière",
        help_text="Ex: Mathématiques, Français"
    )

    class Meta:
        verbose_name = "Matière"
        verbose_name_plural = "Matières"
        ordering = ['id']
        unique_together = ('class_level', 'name')

    def __str__(self):
        return f"{self.name} - {self.class_level}"


class Content(BaseModel):
    """
    Modèle pour les contenus pédagogiques
    """
    CONTENT_TYPE_CHOICES = (
        ('course', 'Cours'),
        ('exam', 'Épreuve'),
        ('correction', 'Correction'),
    )

    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name="contents",
        verbose_name="Matière",
        help_text="Matière associée"
    )
    title = models.CharField(
        max_length=200,
        verbose_name="Titre",
        help_text="Titre du contenu"
    )
    content_type = models.CharField(
        max_length=20,
        choices=CONTENT_TYPE_CHOICES,
        verbose_name="Type de contenu",
        help_text="Cours, épreuve ou correction"
    )
    youtube_url = models.URLField(
        verbose_name="Lien YouTube",
        help_text="Lien vers la vidéo YouTube"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Description",
        help_text="Description du contenu"
    )
    is_published = models.BooleanField(
        default=True,
        verbose_name="Publié",
        help_text="Indique si le contenu est visible"
    )

    class Meta:
        verbose_name = "Contenu"
        verbose_name_plural = "Contenus"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.get_content_type_display()})"

class Comment(BaseModel):
    """
    Modèle pour les commentaires des internautes
    """
    content = models.ForeignKey(
        Content,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Contenu",
        help_text="Contenu commenté"
    )
    author_name = models.CharField(
        max_length=100,
        verbose_name="Nom de l'auteur",
        help_text="Nom de l'internaute"
    )
    message = models.TextField(
        verbose_name="Message",
        help_text="Message du commentaire"
    )
    is_approved = models.BooleanField(
        default=False,
        verbose_name="Approuvé",
        help_text="Commentaire validé par l'administrateur"
    )

    class Meta:
        verbose_name = "Commentaire"
        verbose_name_plural = "Commentaires"
        ordering = ['-created_at']

    def __str__(self):
        return f"Commentaire de {self.author_name}"

class Video(BaseModel):
    """
    Modèle pour les vidéos pédagogiques
    """

    titre = models.CharField(
        max_length=200,
        verbose_name="Titre",
        help_text="Titre de la vidéo pédagogique"
    )

    description = models.TextField(
        blank=True,
        verbose_name="Description",
        help_text="Description de la vidéo"
    )

    lien_youtube = models.URLField(
        verbose_name="Lien YouTube",
        help_text="Lien vers la vidéo YouTube"
    )

    matiere = models.ForeignKey(
        Matiere,
        on_delete=models.CASCADE,
        related_name="videos",
        verbose_name="Matière",
        help_text="Matière associée à la vidéo"
    )

    type_contenu = models.ForeignKey(
        TypeContenu,
        on_delete=models.CASCADE,
        related_name="videos",
        verbose_name="Type de contenu",
        help_text="Type de contenu : cours, épreuve ou correction"
    )

    is_published = models.BooleanField(
        default=True,
        verbose_name="Publié",
        help_text="Indique si la vidéo est visible par les internautes"
    )

    class Meta:
        verbose_name = "Vidéo"
        verbose_name_plural = "Vidéos"
        ordering = ['-created_at']

    def __str__(self):
        return self.titre

