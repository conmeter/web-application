from django.urls import path
from paytm import views as pv

urlpatterns = [
    # Examples:
   path('', pv.home, name='homep'),
    path('payment/', pv.payment, name='payment'),
    path('response/', pv.response, name='response'),
]
