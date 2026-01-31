# core/views.py
from django.views.generic import TemplateView


class HomeView(TemplateView):
    """
    Page d'accueil principale de WilfriedÉducation
    """
    template_name = "pages/index.html"

    # Optionnel : si tu veux passer des données dynamiques plus tard
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Exemples de données que tu pourras ajouter plus tard :
        # context["stats"] = {
        #     "students": 5200,
        #     "courses": 580,
        #     "satisfaction": 98
        # }
        # context["featured_courses"] = Course.objects.filter(is_featured=True)[:6]
        
        return context