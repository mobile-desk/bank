from django.urls import path
from . import views


app_name = 'transactions'

urlpatterns = [
    path('pat/', views.pat, name='pat'),
    path('make-payment/', views.make_payment, name='make_payment'),
    path('verify-code/', views.verify_code, name='verify_code'),
    path('payment-success/', views.payment_success, name='payment_success'),



]
