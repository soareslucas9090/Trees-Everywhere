from django import forms

from .models import Account, Tree, User


class UserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "email",
            "name",
            "password",
            "accounts",
        ]

    accounts = forms.ModelMultipleChoiceField(
        queryset=Account.objects.filter(active=True), required=False
    )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
            self.save_m2m()
            user.accounts.set(self.cleaned_data["accounts"])
        return user


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ["name", "active"]


class TreeForm(forms.ModelForm):
    class Meta:
        model = Tree
        fields = ["name", "scientific_name"]
