from django import forms

from .models import Account, User


class UserCreationForm(forms.ModelForm):
    accounts = forms.ModelMultipleChoiceField(
        queryset=Account.objects.all(), required=False
    )

    class Meta:
        model = User
        fields = [
            "email",
            "name",
            "password",
            "accounts",
        ]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
            self.save_m2m()
            user.accounts.set(self.cleaned_data["accounts"])
        return user
