import json

from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase
from rest_framework.views import status

from order.factories import UserFactory
from product.factories import CategoryFactory, ProductFactory
from product.models import Product


class TestProductViewSet(APITestCase):
    client = APIClient()

    def setUp(self):
        self.user = UserFactory()
        token = Token.objects.create(user=self.user)  # added
        token.save()  # added

        self.product = ProductFactory(
            title="pro controller",
            price=200.00,
        )

    def test_get_all_product(self):
        token = Token.objects.get(user__username=self.user.username)  # added
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + token.key)  # added
        response = self.client.get(
            reverse("product-list", kwargs={"version": "v1"}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        product_data = json.loads(response.content)

        self.assertEqual(product_data["results"]
                         [0]["title"], self.product.title)
        self.assertEqual(product_data["results"]
                         [0]["price"], self.product.price)
        self.assertEqual(product_data["results"]
                         [0]["active"], self.product.active)
        
    def test_create_product(self):
        token = Token.objects.get(user__username=self.user.username)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        category = CategoryFactory()
        data = json.dumps(
            {"title": "notebook", "price": 800.00,
                "categories_id": [category.id]}
        )

        response = self.client.post(
            reverse("product-list", kwargs={"version": "v1"}),
            data=data,
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        created_product = Product.objects.get(title="notebook")

        self.assertEqual(created_product.title, "notebook")
        self.assertEqual(created_product.price, 800.00)

# test: get product by id
    def test_get_single_product(self):
        token = Token.objects.get(user__username=self.user.username) # user authentication
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)

        response = self.client.get(
            reverse("product-detail", kwargs={"version": "v1", "pk": self.product.id}) # gets product passing id, dinamically creates url for endpoint product-detail
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK) # check that requisition worked
        product_data = json.loads(response.content) # convert json string from response into structured dict

        self.assertEqual(product_data["title"], self.product.title) # check if data returned forom api match object created by setup
        self.assertEqual(product_data["price"], self.product.price)

# test: remove product
    def test_delete_product(self):
        token = Token.objects.get(user__username=self.user.username) # user authentication
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)

        response = self.client.delete(
            reverse("product-detail", kwargs={"version": "v1", "pk": self.product.id}) # delete product, finds it by id
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT) # checks that content no longer exists
        self.assertFalse(Product.objects.filter(id=self.product.id).exists()) # fails if product is still in the db