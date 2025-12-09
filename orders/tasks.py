# orders/tasks.py
from celery import shared_task
from django.db import transaction
from .models import Order
from .risk import calculate_risk  # you already have this from previous day

@shared_task
def score_order_async(order_id: int):
    """
    Celery task: load order, calculate risk, save on order.
    """
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return

    result = calculate_risk(order)
    score = result.get("score")
    band = result.get("band")
    reasons_list = result.get("reasons", [])

    reasons_str = ", ".join(reasons_list)

    # Use transaction to be safe
    with transaction.atomic():
        order.risk_score = score
        order.risk_band = band
        order.risk_reasons = reasons_str
        order.save(update_fields=["risk_score", "risk_band", "risk_reasons"])
