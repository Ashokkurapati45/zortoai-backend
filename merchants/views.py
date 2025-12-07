# merchants/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Merchant, APIKey
from .serializers import MerchantSerializer, APIKeyCreateSerializer

class MerchantViewSet(viewsets.ModelViewSet):
    serializer_class = MerchantSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Merchant.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=["post"])
    def create_api_key(self, request, pk=None):
        merchant = self.get_object()
        serializer = APIKeyCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        name = serializer.validated_data.get("name")
        api_obj, raw = APIKey.create_key(merchant=merchant, name=name)
        # raw must be shown only once — merchant should copy/store it securely
        return Response({"api_key": raw, "id": api_obj.id}, status=status.HTTP_201_CREATED)
