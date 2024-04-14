import os
import uuid

from dotenv import load_dotenv, find_dotenv
from rest_framework.response import Response
from rest_framework.views import APIView
from liqpay import LiqPay


load_dotenv(find_dotenv())


def get_liqpay():
    public_key = os.environ.get("PUBLIC_KEY")
    private_key = os.environ.get("PRIVATE_KEY")
    liqpay = LiqPay(public_key, private_key)
    return liqpay


class LiqPayView(APIView):
    def get(self, request):
        liqpay = get_liqpay()
        data = {
            'action'        : 'pay',
            'amount'        : '100.00',
            'currency'      : 'UAH',
            'description'   : 'Опис платежу',
            'order_id'      : uuid.uuid4(),
            'version'       : '3',
            'result_url'    : 'http://yoursite.com/result/',
            'server_url'    : 'http://yoursite.com/notify/'
        }
        signature = liqpay.cnb_signature(data)
        data['signature'] = signature
        return Response(data)
