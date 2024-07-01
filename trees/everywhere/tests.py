from decimal import Decimal

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.test import Client, TestCase
from django.urls import reverse

from .models import Account, Account_User, PlantedTree, Tree

User = get_user_model()


class PlantedTreeListViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email="user@example.com", name="testuser", password="password123"
        )
        self.account = Account.objects.create(name="Test Account")
        self.tree = Tree.objects.create(
            name="Test Tree", scientific_name="Testus treeus"
        )
        self.planted_tree = PlantedTree.objects.create(
            age=5,
            user=self.user,
            tree=self.tree,
            account=self.account,
            latitude=Decimal("10.1"),
            longitude=Decimal("20.2"),
        )

    def test_planted_tree_list_view(self):
        self.client.login(email="user@example.com", password="password123")
        response = self.client.get(reverse("planted_trees_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "user/lists/planted_tree_list.html")
        self.assertContains(response, self.tree.name)
