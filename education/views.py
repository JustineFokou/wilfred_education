# education/views.py
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, RedirectView, TemplateView
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages

from .forms import UserCreateForm, UserUpdateForm

User = get_user_model()

# Configuration des onglets : titre, sous-titre, template, optionnellement context_key + queryset
TAB_CONFIG = {
    "dashboard": {
        "title": "Tableau de bord",
        "subtitle": "Vue d'ensemble et statistiques",
        "template": "admin/tab_content.html",
    },
    "users": {
        "title": "Gestion des utilisateurs",
        "subtitle": "Créer, modifier et gérer les comptes",
        "template": "admin/users_list.html",
        "context_key": "users",
        "queryset": lambda: User.objects.all().order_by("-date_joined"),
    },
    "errors": {
        "title": "Erreurs et logs",
        "subtitle": "Suivi des erreurs et journaux système",
        "template": "admin/tab_content.html",
    },
    "settings": {
        "title": "Paramètres",
        "subtitle": "Configuration générale de l'application",
        "template": "admin/tab_content.html",
    },
}

DEFAULT_TAB = "dashboard"


def get_tab_config(tab_key):
    return TAB_CONFIG.get(tab_key, TAB_CONFIG[DEFAULT_TAB])


class AdminDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    """Vue admin : template et contexte pilotés par ?tab= et TAB_CONFIG."""

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def get_template_names(self):
        tab = self.request.GET.get("tab", DEFAULT_TAB)
        config = get_tab_config(tab)
        return [config["template"]]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tab = self.request.GET.get("tab", DEFAULT_TAB)
        config = get_tab_config(tab)

        context["tab"] = tab
        context["page_title"] = config["title"]
        context["page_sub"] = config["subtitle"]
        context["user_count"] = User.objects.filter(is_active=True).count()
        context["available_tabs"] = [
            {"key": key, "title": cfg["title"]} for key, cfg in TAB_CONFIG.items()
        ]

        if tab == "dashboard":
            try:
                from education.models import Content
                context["content_count"] = Content.objects.filter(is_published=True).count()
                context["stats"] = {
                    "users": context["user_count"],
                    "content": context["content_count"],
                }
                # Répartition des rôles (dynamique)
                from django.db.models import Count
                role_counts = User.objects.filter(is_active=True).values("role").annotate(count=Count("id"))
                breakdown = {r["role"]: r["count"] for r in role_counts}
                role_labels = dict(User.ROLE_CHOICES)
                context["role_breakdown"] = [
                    {"role": r, "label": role_labels.get(r, r), "count": breakdown.get(r, 0)}
                    for r, _ in User.ROLE_CHOICES
                ]
            except Exception:
                context["content_count"] = 0
                context["stats"] = {"users": context["user_count"], "content": 0}
                context["role_breakdown"] = []

        context_key = config.get("context_key")
        queryset = config.get("queryset")
        if context_key and callable(queryset):
            qs = queryset()
            if tab == "users":
                role = self.request.GET.get("role")
                if role and role != "all":
                    qs = qs.filter(role=role)
                context["current_role_filter"] = role or "all"
            context[context_key] = qs

        return context


class UserCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """Création d'un utilisateur (admin)."""

    model = User
    form_class = UserCreateForm
    template_name = "admin/user_form.html"
    success_url = reverse_lazy("admin:dashboard")
    extra_context = {"page_title": "Nouvel utilisateur", "page_sub": "Créer un compte utilisateur"}

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def form_valid(self, form):
        messages.success(self.request, "Utilisateur créé avec succès.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("admin:dashboard") + "?tab=users"


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Édition d'un utilisateur (admin)."""

    model = User
    form_class = UserUpdateForm
    template_name = "admin/user_form.html"
    context_object_name = "user_obj"
    pk_url_kwarg = "pk"

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = f"Modifier — {self.object.get_full_name()}"
        context["page_sub"] = "Modifier les informations du compte"
        return context

    def form_valid(self, form):
        messages.success(self.request, "Utilisateur mis à jour.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("admin:dashboard") + "?tab=users"
