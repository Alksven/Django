from django.contrib.auth.models import User, Permission
from django.test import TestCase
from django.urls import reverse

from string import ascii_letters
from random import choices

from shopapp.models import Product


class ProductCreateViewTestCase(TestCase):

    def setUp(self):
        self.product_name = "".join(choices(ascii_letters, k=10))
        Product.objects.filter(name=self.product_name).delete()

        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        add_product_permission = Permission.objects.get(codename='add_product')
        self.user.user_permissions.set([add_product_permission])

    def test_product_create_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(
            reverse("shopapp:product_create"),
            {
                "name": self.product_name,
                "price": "1234",
                "description": "Table444, Table444",
                "diccount": "0",
            }
        )
        self.assertRedirects(response, reverse("shopapp:products_list"))
        Product.objects.filter(name=self.product_name).exists()


class ProductDetailsViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create(username='testuser')
        cls.product = Product.objects.create(name="Best Product", created_by=cls.user)

    @classmethod
    def tearDownClass(cls):
        cls.product.delete()

    def test_get_product(self):
        response = self.client.get(reverse("shopapp:products_details", kwargs={"pk": self.product.pk}))
        self.assertEquals(response.status_code, 200)

    def test_get_product_andcontent(self):
        response = self.client.get(reverse("shopapp:products_details", kwargs={"pk": self.product.pk}))
        self.assertContains(response, self.product.name)