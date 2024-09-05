from django.db import models
from django.conf import settings

from order.models import Order


class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')
    session_id = models.CharField(max_length=255, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, default="PENDING")
    created_at = models.DateTimeField(auto_now_add=True)

    def complete(self):
        self.status = 'PAID'
        self.save()

    def __str__(self):
        return f"Payment for Order {self.order.id} - Status: {self.status}"
