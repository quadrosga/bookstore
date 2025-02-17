import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework.authtoken.models import Token

from order.factories import OrderFactory, UserFactory
from order.models import Order
from product.factories import CategoryFactory, ProductFactory


class TestOrderViewSet(APITestCase):

    client = APIClient()

    def setUp(self):
        self.user = UserFactory() # create user
        token = Token.objects.create(user=self.user) # create token
        token.save() # save token

        self.category = CategoryFactory(title="technology")
        self.product = ProductFactory(
            title="mouse", price=100, category=[self.category]
        )
        self.order = OrderFactory(product=[self.product])

    def test_order(self):
        token = Token.objects.get(user__username=self.user.username)  # get user token created in setUp
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + token.key)  # add auth token to header
        response = self.client.get(
            reverse("order-list", kwargs={"version": "v1"}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        order_data = json.loads(response.content)
        self.assertEqual(
            order_data["results"][0]["product"][0]["title"], self.product.title
        )
        self.assertEqual(
            order_data["results"][0]["product"][0]["price"], self.product.price
        )
        self.assertEqual(
            order_data["results"][0]["product"][0]["active"], self.product.active
        )
        self.assertEqual(
            order_data["results"][0]["product"][0]["category"][0]["title"],
            self.category.title,
        )

    def test_create_order(self):
        token = Token.objects.get(user__username=self.user.username)  # get user token
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + token.key)  # add auth token to header
        
        product = ProductFactory()
        data = json.dumps({"products_id": [product.id], "user": self.user.id})

        response = self.client.post(
            reverse("order-list", kwargs={"version": "v1"}),
            data=data,
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        created_order = Order.objects.get(user=self.user)

# test: get order by id
    def test_get_single_order(self):
        token = Token.objects.get(user__username=self.user.username)  # get user token
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + token.key)  # credentials
        response = self.client.get(
            reverse("order-detail", kwargs={"version": "v1", "pk": self.order.id})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        order_data = json.loads(response.content)
        self.assertEqual(order_data["product"][0]["title"], self.product.title)

# test: remove order by id
    def test_delete_order(self):
        token = Token.objects.get(user__username=self.user.username)  # get user token
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + token.key)  # add auth token to header
        response = self.client.delete(
            reverse("order-detail", kwargs={"version": "v1", "pk": self.order.id})
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Order.objects.filter(id=self.order.id).exists())