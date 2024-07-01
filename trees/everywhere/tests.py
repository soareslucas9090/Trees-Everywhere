from decimal import Decimal

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.test import Client, TestCase
from django.urls import reverse

from .models import Account, Account_User, PlantedTree, Tree

User = get_user_model()


class PlantedTreeListViewTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = Client()
        ### Data to test 1 ###
        cls.user1 = User.objects.create_user(
            email="user1@youshop.com", name="testuser1", password="password123"
        )
        cls.account = Account.objects.create(name="Test Account 1")
        cls.user1.accounts.add(cls.account)
        cls.tree = Tree.objects.create(
            name="Test Tree 1", scientific_name="Testus treeus 1"
        )
        cls.planted_tree = PlantedTree.objects.create(
            age=5,
            user=cls.user1,
            tree=cls.tree,
            account=cls.user1.accounts.first(),
            latitude=Decimal("10.1"),
            longitude=Decimal("20.2"),
        )
        ### Data to test 2 ###
        cls.user2 = User.objects.create_user(
            email="user2@youshop.com", name="testuser1", password="password123"
        )
        cls.user2.accounts.add(cls.account)

    def test_planted_tree_list_view(self):
        self.client.login(email="user1@youshop.com", password="password123")
        response = self.client.get(reverse("planted_trees_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "user/lists/planted_tree_list.html")
        self.assertContains(response, self.tree.name)

    def test_planted_tree_list_account_view(self):
        self.client.login(email="user2@youshop.com", password="password123")
        response = self.client.get(reverse("planted_trees_list_account"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "user/lists/planted_tree_list_account.html")
        self.assertContains(response, self.tree.name)
        self.assertContains(response, self.user1.name)


"""
class PlantedTreeAccountsViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email="user@example.com", name="testuser", password="password123"
        )
        self.account = Account.objects.create(name="Test Account")
        self.user.accounts.add(self.account)
        self.client.login(email="user@example.com", password="password123")
        self.other_user = User.objects.create_user(
            email="otheruser@example.com", name="otheruser", password="password123"
        )
        self.tree = Tree.objects.create(
            name="Test Tree", scientific_name="Testus treeus"
        )
        self.planted_tree = PlantedTree.objects.create(
            age=5,
            user=self.other_user,
            tree=self.tree,
            account=self.account,
            latitude=Decimal("10.1"),
            longitude=Decimal("20.2"),
        )

    def test_planted_tree_accounts_view(self):
        response = self.client.get(reverse("planted_trees_list_account"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "user/lists/planted_tree_list_account.html")
        self.assertContains(response, self.tree.name)
"""
