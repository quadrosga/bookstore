#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.test import TestCase

from order.factories import OrderFactory, ProductFactory
from order.serializers import OrderSerializer


class TestOrderSerializer(TestCase):
    def setUp(self) -> None:
        self.product_1 = ProductFactory()  # Cria instancia 1 de product
        self.product_2 = ProductFactory()  # Cria instancia 2 de product

        self.order = OrderFactory(
            product=(self.product_1, self.product_2)
        )  # Cria uma instancia de order que inclui os 2 products criados
        self.order_serializer = OrderSerializer(self.order)  # Serializa o objeto order

    def test_order_serializer(self):
        serializer_data = self.order_serializer.data  # Armazena os dados serializados
        self.assertEquals(serializer_data["product"][0]["title"], self.product_1.title)
        self.assertEquals(serializer_data["product"][1]["title"], self.product_2.title)
        # Verificam se os títulos das listas serializadas batem com os títulos dos objetos
