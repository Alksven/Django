from string import ascii_letters
from random import choices

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