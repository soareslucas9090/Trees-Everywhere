from django import forms

from .models import Account, PlantedTree, Tree, User


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


class PlantedTreeForm(forms.ModelForm):
    class Meta:
        model = PlantedTree
        fields = ["age", "tree", "account"]

    def get_form(self):
        if self.is_valid():
            data = self.cleaned_data
            return data
        else:
            return None

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super(PlantedTreeForm, self).__init__(*args, **kwargs)

        if user:
            self.fields["account"].queryset = Account.objects.filter(
                accountuser_account__user=user
            )

    tree = forms.ModelChoiceField(queryset=Tree.objects.all(), required=True)
