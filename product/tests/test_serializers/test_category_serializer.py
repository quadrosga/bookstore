from django.test import TestCase

from product.factories import CategoryFactory
from product.serializers import CategorySerializer


# Criando uma instancia de categoria
# e testando a serialização do objeto
class TestCategorySerializer(TestCase):
    def setUp(self) -> None:
        self.category = CategoryFactory(title="fantasy")  # Cria a categoria fantasy
        self.category_serializer = CategorySerializer(
            self.category
        )  # Serializa o objeto

    def test_order_serializer(self):
        serializer_data = (
            self.category_serializer.data
        )  # Armazena os dados serializados

        self.assertEquals(
            serializer_data["title"], "fantasy"
        )  # Verifica de o título da categoria é fantasy
