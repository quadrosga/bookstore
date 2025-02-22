from rest_framework.viewsets import ModelViewSet

from order.models import Order
from order.serializers import OrderSerializer
from rest_framework.authentication import (
    SessionAuthentication,
    BasicAuthentication,
    TokenAuthentication,
)
from rest_framework.permissions import IsAuthenticated


class OrderViewSet(ModelViewSet):
    serializer_class = OrderSerializer
    authentication_classes = [
        SessionAuthentication,
        BasicAuthentication,
        TokenAuthentication,
    ]
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all().order_by("id")
