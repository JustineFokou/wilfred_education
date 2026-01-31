from django.db import models
from core.models import BaseModel

class Level(BaseModel):
    """
    School levels (Primary, Secondary, Higher)
    """
    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Level name",
        help_text="Example: Primary, Secondary, Higher"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Description",
        help_text="Level description"
    )

    class Meta:
        verbose_name = "Level"
        verbose_name_plural = "Levels"
        ordering = ["id"]

    def __str__(self):
        return self.name



class ClassLevel(BaseModel):
    """
    School classes
    """
    level = models.ForeignKey(
        Level,
        on_delete=models.CASCADE,
        related_name="classes",
        verbose_name="Level"
    )
    name = models.CharField(
        max_length=50,
        verbose_name="Class name",
        help_text="Example: CP, CE1, 6th, Terminale, L1"
    )

    class Meta:
        verbose_name = "Class"
        verbose_name_plural = "Classes"
        ordering = ["id"]
        unique_together = ("level", "name")

    def __str__(self):
        return f"{self.name} ({self.level.name})"


class Subject(BaseModel):
    """
    School subjects
    """
    class_level = models.ForeignKey(
        ClassLevel,
        on_delete=models.CASCADE,
        related_name="subjects",
        verbose_name="Class"
    )
    name = models.CharField(
        max_length=100,
        verbose_name="Subject name",
        help_text="Example: Mathematics, French"
    )

    class Meta:
        verbose_name = "Subject"
        verbose_name_plural = "Subjects"
        ordering = ["id"]
        unique_together = ("class_level", "name")

    def __str__(self):
        return f"{self.name} - {self.class_level}"

class Content(BaseModel):
    """
    Educational content
    """

    CONTENT_TYPE_CHOICES = (
        ("course", "Course"),
        ("exam", "Exam"),
        ("correction", "Correction"),
    )

    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name="contents",
        verbose_name="Subject"
    )
    title = models.CharField(
        max_length=200,
        verbose_name="Title"
    )
    content_type = models.CharField(
        max_length=20,
        choices=CONTENT_TYPE_CHOICES,
        verbose_name="Content type"
    )
    youtube_url = models.URLField(
        verbose_name="YouTube link"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Description"
    )
    is_published = models.BooleanField(
        default=True,
        verbose_name="Published"
    )

    class Meta:
        verbose_name = "Content"
        verbose_name_plural = "Contents"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} ({self.get_content_type_display()})"

class Comment(BaseModel):
    """
    User comments
    """
    content = models.ForeignKey(
        Content,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Content"
    )
    author_name = models.CharField(
        max_length=100,
        verbose_name="Author name"
    )
    message = models.TextField(
        verbose_name="Message"
    )
    is_approved = models.BooleanField(
        default=False,
        verbose_name="Approved"
    )

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Comment by {self.author_name}"

    

class Video(BaseModel):
    """
    Educational videos
    """

    title = models.CharField(
        max_length=200,
        verbose_name="Title"
    )

    description = models.TextField(
        blank=True,
        verbose_name="Description"
    )

    youtube_link = models.URLField(
        verbose_name="YouTube link"
    )

    content = models.ForeignKey(
        Content,
        on_delete=models.CASCADE,
        related_name="videos",
        verbose_name="Content",
        help_text="Related educational content"
    )

    is_published = models.BooleanField(
        default=True,
        verbose_name="Published"
    )

    class Meta:
        verbose_name = "Video"
        verbose_name_plural = "Videos"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

