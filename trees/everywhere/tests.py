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
        cls.account1 = Account.objects.create(name="Test Account 1")
        cls.user1.accounts.add(cls.account1)
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
        ### Data to test 1 ###

        ### Data to test 2 ###
        cls.admin = User.objects.create_user(
            email="admin@youshop.com",
            name="admin",
            password="password123",
            is_admin=True,
        )
        ### Data to test 2 ###

        ### Data to test 3 ###
        cls.user2 = User.objects.create_user(
            email="user2@youshop.com", name="testuser2", password="password123"
        )
        cls.user2.accounts.add(cls.account1)
        ### Data to test 3 ###

        ### Data to test 4 ###
        cls.user3 = User.objects.create_user(
            email="user3@youshop.com", name="testuser2", password="password123"
        )
        cls.account2 = Account.objects.create(name="Test Account 2")
        cls.user3.accounts.add(cls.account2)
        cls.tree2 = Tree.objects.create(
            name="Test Tree 2", scientific_name="Testus treeus 2"
        )
        cls.tree3 = Tree.objects.create(
            name="Test Tree 2", scientific_name="Testus treeus 2"
        )
        cls.tree4 = Tree.objects.create(
            name="Test Tree 2", scientific_name="Testus treeus 2"
        )
        ### Data to test 4 ###

    # Test 1:
    def test_planted_tree_list_view(self):
        self.client.login(email="user1@youshop.com", password="password123")
        response = self.client.get(reverse("planted_trees_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "user/lists/planted_tree_list.html")
        self.assertContains(response, self.tree.name)

    # Test 2 is not possible as described, as the user id is taken directly from request.user.id,
    # leaving no room for a user to try to access data from others, so it replaces the test
    # requested by a user trying to access an admin page and vice-versa
    # Teste 2:
    def test_error_403(self):
        self.client.login(email="admin@youshop.com", password="password123")
        response = self.client.get(reverse("menu_admin"))
        self.assertEqual(response.status_code, 200)
        self.client.logout()
        self.client.login(email="user1@youshop.com", password="password123")
        response = self.client.get(reverse("menu_admin"))
        self.assertEqual(response.status_code, 403)

    # Test 3
    def test_planted_tree_list_account_view(self):
        self.client.login(email="user2@youshop.com", password="password123")
        response = self.client.get(reverse("planted_trees_list_account"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "user/lists/planted_tree_list_account.html")
        self.assertContains(response, self.tree.name)
        self.assertContains(response, self.user1.name)

    # Test 4
    def test_plant_tree(self):
        initial_count = PlantedTree.objects.count()
        self.user3.plant_tree(
            tree=self.tree2,
            account=self.user3.accounts.first(),
            age=5,
            location=[Decimal("10.1"), Decimal("20.2")],
        )

        planted_tree_test = PlantedTree.objects.last()

        self.assertEqual(PlantedTree.objects.count(), (initial_count + 1))
        self.assertEqual(planted_tree_test.user, self.user3)
        self.assertEqual(planted_tree_test.tree, self.tree2)
        self.assertEqual(planted_tree_test.account, self.account2)
        self.assertEqual(planted_tree_test.age, 5)
        self.assertEqual(planted_tree_test.latitude, Decimal("10.1"))
        self.assertEqual(planted_tree_test.longitude, Decimal("20.2"))

        # The newly inserted tree is deleted to test mass insertion
        tree_to_delete = PlantedTree.objects.filter(user=self.user3)
        tree_to_delete.delete()

        initial_count_2 = PlantedTree.objects.count()

        trees_to_plant = [
            {
                "tree": self.tree3,
                "account": self.user3.accounts.first(),
                "age": 5,
                "location": [Decimal("10.1"), Decimal("20.2")],
            },
            {
                "tree": self.tree4,
                "account": self.user3.accounts.first(),
                "age": 4,
                "location": [Decimal("11.1"), Decimal("22.2")],
            },
        ]

        self.user3.plant_trees(trees_to_plant)

        self.assertEqual(
            PlantedTree.objects.count(), initial_count_2 + len(trees_to_plant)
        )

        # Index used to iterate under the list of "trees_to_plant"
        i = 0
        for tree_data in PlantedTree.objects.filter(user=self.user3):
            self.assertEqual(trees_to_plant[i]["tree"], tree_data.tree)
            self.assertEqual(trees_to_plant[i]["account"], tree_data.account)
            self.assertEqual(trees_to_plant[i]["age"], tree_data.age)
            # Remembering that "location" is a list
            self.assertEqual(trees_to_plant[i]["location"][0], tree_data.latitude)
            self.assertEqual(trees_to_plant[i]["location"][1], tree_data.longitude)
            i += 1
