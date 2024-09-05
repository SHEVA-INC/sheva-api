import os

import requests
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from order.models import Order
from .models import Payment


from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())

class InitiatePaymentView(APIView):
    def post(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

        # Створення нового платежу
        payment = Payment.objects.create(order=order, amount=order.total_price, status='INITIATED')

        headers = {
            'X-Token': os.environ.get('MONO_TOKEN'),
            'Content-Type': 'application/json',
        }
        data = {
            'amount': int(payment.order.total_price * 100),
            'currency': 'UAH',
            'redirectUrl': 'https://yourwebsite.com/success/',
            'webhookUrl': 'https://yourwebsite.com/api/v1/payments/webhook/',
            'reference': str(payment.order.id),
        }
        response = requests.post('https://api.monobank.ua/api/merchant/invoice/create',
                                 headers=headers, json=data)

        if response.status_code == 200:
            response_data = response.json()
            payment.session_id = response_data.get('invoiceId')
            payment.save()
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response(response.json(), status=response.status_code)


class MonobankWebhookView(APIView):
    def post(self, request):
        data = request.data

        if 'invoiceId' not in data or 'status' not in data:
            return JsonResponse({'error': 'Invalid data'}, status=400)

        invoice_id = data['invoiceId']
        status = data['status']

        try:
            payment = Payment.objects.get(session_id=invoice_id)
            if status == 'success':
                payment.complete()
            else:
                payment.status = 'FAILED'
                payment.save()
            return JsonResponse({'message': 'Payment status updated successfully'}, status=200)
        except Payment.DoesNotExist:
            return JsonResponse({'error': 'Payment not found'}, status=404)