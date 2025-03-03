import json

from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework.views import status

from product.factories import CategoryFactory
from product.models import Category


class CategoryViewSet(APITestCase):
    client = APIClient()

    def setUp(self):
        self.category = CategoryFactory(title="books")

    def test_get_all_category(self):
        response = self.client.get(reverse("category-list", kwargs={"version": "v1"}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        category_data = json.loads(response.content)

        self.assertEqual(category_data["results"][0]["title"], self.category.title)

    def test_create_category(self):
        data = json.dumps({"title": "technology"})

        response = self.client.post(
            reverse("category-list", kwargs={"version": "v1"}),
            data=data,
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        created_category = Category.objects.get(title="technology")

        self.assertEqual(created_category.title, "technology")

    # test: get category by id
    def test_get_single_category(self):
        response = self.client.get(
            reverse(
                "category-detail", kwargs={"version": "v1", "pk": self.category.id}
            )  # gets a category by id, dynamically creates url of endpoint category-detail
        )

        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )  # checks that requisition is successful
        category_data = json.loads(
            response.content
        )  ## convert json string from response into structured dict

        self.assertEqual(
            category_data["title"], self.category.title
        )  # checks that data returned from api = object created by setup

    # test: remove category
    def test_delete_category(self):
        response = self.client.delete(
            reverse(
                "category-detail", kwargs={"version": "v1", "pk": self.category.id}
            )  # deletes category by its id
        )

        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )  # checks that category has been removed
        self.assertFalse(
            Category.objects.filter(id=self.category.id).exists()
        )  # checks that it no longer exists in db
