# accounts/views/register.py
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.core.exceptions import ValidationError
from ..models import User


class RegisterView(TemplateView):
    template_name = 'auth/register.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # On passe des placeholders et classes pour garder le style cohérent
        context.update({
            'form_classes': {
                'first_name': 'w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-accent-500 focus:ring-2 focus:ring-accent-200 transition-all duration-200 outline-none',
                'last_name':  'w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-accent-500 focus:ring-2 focus:ring-accent-200 transition-all duration-200 outline-none',
                'email':      'w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-accent-500 focus:ring-2 focus:ring-accent-200 transition-all duration-200 outline-none',
                'phone':      'w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-accent-500 focus:ring-2 focus:ring-accent-200 transition-all duration-200 outline-none',
                'password':   'w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-accent-500 focus:ring-2 focus:ring-accent-200 transition-all duration-200 outline-none pr-12',
                'password_confirm': 'w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-accent-500 focus:ring-2 focus:ring-accent-200 transition-all duration-200 outline-none pr-12',
            },
            'placeholders': {
                'first_name': 'Jean',
                'last_name':  'Dupont',
                'email':      'votre@email.com',
                'phone':      '+237 XXX XXX XXX',
            }
        })
        return context

    def post(self, request, *args, **kwargs):
        # Récupération des données du formulaire
        first_name = request.POST.get('first_name', '').strip()
        last_name  = request.POST.get('last_name', '').strip()
        email      = request.POST.get('email', '').strip()
        phone      = request.POST.get('phone', '').strip()
        password   = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

        errors = []

        # Validations de base (côté serveur)
        if not first_name:
            errors.append("Le prénom est requis.")
        if not last_name:
            errors.append("Le nom est requis.")
        if not email:
            errors.append("L'email est requis.")
        if password != password_confirm:
            errors.append("Les mots de passe ne correspondent pas.")
        if len(password) < 8:
            errors.append("Le mot de passe doit contenir au moins 8 caractères.")
        if User.objects.filter(email=email).exists():
            errors.append("Cet email est déjà utilisé.")

        # Si erreurs → on renvoie avec les messages
        if errors:
            for err in errors:
                messages.error(request, err)
            # On repasse les valeurs saisies pour pré-remplir
            context = self.get_context_data()
            context.update({
                'old': {
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': email,
                    'phone': phone,
                }
            })
            return render(request, self.template_name, context)

        # Création de l'utilisateur
        try:
            user = User.objects.create_user(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                phone=phone,
            )
            # Connexion automatique
            login(request, user)
            messages.success(request, "Compte créé avec succès ! Bienvenue 🎉")
            return redirect('home')  # ← adapte selon ton URL d'accueil

        except ValidationError as e:
            messages.error(request, str(e))
            context = self.get_context_data()
            context['old'] = {
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'phone': phone,
            }
            return render(request, self.template_name, context)