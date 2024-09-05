from django.urls import path
from .views import InitiatePaymentView, MonobankWebhookView

urlpatterns = [
    path('create/<int:order_id>/', InitiatePaymentView.as_view(), name='initiate_payment'),
    path('webhook/', MonobankWebhookView.as_view(), name='monobank_webhook'),
]

app_name = "payment"