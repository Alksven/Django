from string import ascii_letters
from random import choices

from django.conf import settings

from django.contrib.auth.models import Permission, User
from django.test import Client

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from shopapp.utils import add_two_numbers

from shopapp.models import Product


class AddTwoNumbersTestCase(TestCase):
    def test_add_two_numbers(self):
        result = add_two_numbers(2, 3)
        self.assertEquals(result, 5)


class ProductCreateViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpass'
        )
        self.user.user_permissions.add(Permission.objects.get(codename='add_product'))
        self.client.force_login(self.user)

        self.product_name = "".join(choices(ascii_letters, k=10))
        Product.objects.filter(name=self.product_name).delete()

    def test_product_create_view(self):
        response = self.client.post(
            reverse("shopapp:product_create"),
            {
                "name": self.product_name,
                "price": "123.45",
                "description": "a good table",
                "diccount": "10"
            }
        )
        self.assertRedirects(response, reverse("shopapp:products_list"))
        self.assertTrue(
            Product.objects.filter(name=self.product_name).exists()
        )


class ProductDetailsViewTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = Client()
        cls.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpass'
        )
        cls.client.force_login(cls.user)

        cls.product = Product.objects.create(name="Best Product", created_by=cls.user)

    @classmethod
    def tearDownClass(cls):
        cls.product.delete()

    def test_product_details_view(self):
        response = self.client.get(
            reverse("shopapp:products_details", kwargs={"pk": self.product.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_product_and_check_content(self):
        response = self.client.get(
            reverse("shopapp:products_details", kwargs={"pk": self.product.pk})
        )
        self.assertContains(response, self.product.name)


class ProductsListViewTestCase(TestCase):
    fixtures = [
        "products-fixture.json",
    ]

    def test_products(self):
        resource = self.client.get(reverse("shopapp:products_list"))
        self.assertQuerysetEqual(
            qs=Product.objects.filter(archived=False).all(),
            values=(p.pk for p in resource.context["products"]),
            transform=lambda p: p.pk
        )
        self.assertTemplateUsed(resource, "shopapp/products-list.html")


class OrderListViewTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(username="TestUser", password="TestPassword")

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self):
        self.client.force_login(self.user)

    def test_order_list_view(self):
        response = self.client.get(reverse("shopapp:orders_list"))
        self.assertContains(response, "Orders")

    def test_order_list_view_not_authenticated(self):
        self.client.logout()
        response = self.client.get(reverse("shopapp:orders_list"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(str(settings.LOGIN_URL), response.url)






