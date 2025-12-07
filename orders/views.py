# orders/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from merchants.authentication import ApiKeyAuthentication
from .serializers import OrderIngestSerializer
from .models import Order

class OrderIngestView(APIView):
    """
    Public ingestion endpoint for stores to send COD orders.
    Auth: API key only.
    """
    authentication_classes = [ApiKeyAuthentication]
    permission_classes = [IsAuthenticated]  # user is merchant.owner via API key

    def post(self, request):
        merchant = getattr(request, "merchant", None)
        if merchant is None:
            return Response({"detail": "Merchant context missing."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = OrderIngestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        order = Order.objects.create(
            merchant=merchant,
            order_id=serializer.validated_data["order_id"],
            amount=serializer.validated_data.get("amount") or 0,
            pincode=serializer.validated_data.get("pincode"),
        )

        output = OrderIngestSerializer(order)
        return Response(output.data, status=status.HTTP_201_CREATED)
