# core/views.py
from django.views.generic import TemplateView
from django.contrib.auth import get_user_model

User = get_user_model()


class HomeView(TemplateView):
    """Page d'accueil principale."""

    template_name = "pages/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_count"] = User.objects.filter(is_active=True).count()
        try:
            from education.models import Content
            context["content_count"] = Content.objects.filter(is_published=True).count()
        except Exception:
            context["content_count"] = 0
        return context


class CoursView(TemplateView):
    """Page Cours / Niveaux : liste des niveaux et contenus publiés."""

    template_name = "pages/cours.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            from education.models import Level, Content
            levels = Level.objects.filter(is_active=True).order_by("id")
            level_data = []
            for level in levels:
                count = Content.objects.filter(
                    is_published=True,
                    subject__class_level__level=level,
                ).count()
                level_data.append({"level": level, "content_count": count})
            context["level_data"] = level_data
            context["content_count"] = Content.objects.filter(is_published=True).count()
        except Exception:
            context["level_data"] = []
            context["content_count"] = 0
        context["user_count"] = User.objects.filter(is_active=True).count()
        return context