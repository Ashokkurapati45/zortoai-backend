# orders/urls.py
from django.urls import path
from .views import OrderIngestView

urlpatterns = [
    path("orders/", OrderIngestView.as_view(), name="order_ingest"),
]
