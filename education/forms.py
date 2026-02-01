# education/forms.py
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class UserCreateForm(forms.ModelForm):
    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={"placeholder": "Mot de passe temporaire"}),
        required=True,
        min_length=8,
    )

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "phone", "role", "is_active")
        widgets = {
            "first_name": forms.TextInput(attrs={"placeholder": "Prénom"}),
            "last_name": forms.TextInput(attrs={"placeholder": "Nom"}),
            "email": forms.EmailInput(attrs={"placeholder": "email@exemple.com"}),
            "phone": forms.TextInput(attrs={"placeholder": "+237 XXX XXX XXX"}),
            "role": forms.Select(attrs={"class": "form-select"}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserUpdateForm(forms.ModelForm):
    password = forms.CharField(
        label="Nouveau mot de passe (optionnel)",
        widget=forms.PasswordInput(attrs={"placeholder": "Laisser vide pour ne pas changer"}),
        required=False,
        min_length=8,
    )

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "phone", "role", "is_active")
        widgets = {
            "first_name": forms.TextInput(attrs={"placeholder": "Prénom"}),
            "last_name": forms.TextInput(attrs={"placeholder": "Nom"}),
            "email": forms.EmailInput(attrs={"placeholder": "email@exemple.com"}),
            "phone": forms.TextInput(attrs={"placeholder": "+237 XXX XXX XXX"}),
            "role": forms.Select(attrs={"class": "form-select"}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password")
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user
