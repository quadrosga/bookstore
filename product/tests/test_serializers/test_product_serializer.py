from django.test import TestCase

from product.factories import CategoryFactory, ProductFactory
from product.serializers import ProductSerializer


# Criando categoria, instancia (produto)
# e testando a serialização do objeto
class TestProductSerializer(TestCase):
    def setUp(self) -> None:
        self.category = CategoryFactory(title="language learning")  # Cria uma categoria
        self.product_1 = ProductFactory(
            title="german travel guide",
            price=55,
            category=[self.category],  # Cria uma instancia
        )
        self.product_serializer = ProductSerializer(
            self.product_1
        )  # Serializa o objeto

    def test_product_serializer(self):
        serializer_data = self.product_serializer.data
        self.assertEquals(
            serializer_data["price"], 55
        )  # Verifica se o preço retornado pelo serializer é 55
        self.assertEquals(
            serializer_data["title"], "german travel guide"
        )  # Verifica se o preço retornado pelo serializer é german travel guide
        self.assertEquals(
            serializer_data["category"][0]["title"], "language learning"
        )  # Verifica se título da primeira categoria na lista category é language learning
