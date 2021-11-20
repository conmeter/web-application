from django.shortcuts import render
from django.http import HttpResponse
from django.utils.translation import get_language
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.conf import settings
from users.models import User, Issue
from . import Checksum
from django.shortcuts import get_object_or_404, redirect

from paytm.models import PaytmHistory


# Create your views here.

@login_required
def home(request):
    return HttpResponse("<html><a href='" + settings.HOST_URL + "/paytm/payment'>PayNow</html>")


@login_required
def payment(request):
    if request.method == "POST":
        amount = request.POST['amt']
        MERCHANT_KEY = settings.PAYTM_MERCHANT_KEY
        MERCHANT_ID = settings.PAYTM_MERCHANT_ID
        order_id = Checksum.__id_generator__()
        bill_amount = amount
        if bill_amount:
            data_dict = {
                'MID': MERCHANT_ID,
                'ORDER_ID': order_id,
                'TXN_AMOUNT': str(bill_amount),
                'CUST_ID': str(request.user.email),
                'INDUSTRY_TYPE_ID': 'Retail',
                'WEBSITE': 'DEFAULT',
                'CHANNEL_ID': 'WEB',
                'CALLBACK_URL': 'https://www.conmeter.com/paytm/response/',
            }
            param_dict = data_dict
            param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(data_dict, settings.PAYTM_MERCHANT_KEY)
            PaytmHistory(made_by=request.user, amount=bill_amount, order_id=order_id).save()
            return render(request, "paytm/payments.html", {'paytmdict': param_dict})
    else:
        return render(request, 'page/donate.html')


@csrf_exempt
def response(request):
    if request.method == "POST":
        MERCHANT_KEY = settings.PAYTM_MERCHANT_KEY
        data_dict = {}
        for key in request.POST:
            data_dict[key] = request.POST[key]
        verify = Checksum.verify_checksum(data_dict, MERCHANT_KEY, data_dict['CHECKSUMHASH'])
        if verify:
            PaytmHistory.objects.all().filter(order_id=data_dict["ORDERID"]).update(status=data_dict['STATUS'])
            return render(request, "paytm/response.html", data_dict)
        else:
            return HttpResponse("checksum verify failed")
    return HttpResponse(status=200)
