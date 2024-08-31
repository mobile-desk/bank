from django.urls import path
from . import views


app_name = 'transactions'

urlpatterns = [
    path('pat/', views.pat, name='pat'),
    path('make-payment/', views.make_payment, name='make_payment'),
    path('verify-transaction/', views.verify_transaction, name='verify_transaction'),
    path('transactions/', views.transaction_list, name='transaction_list'),
    path('receipt/<uuid:receipt_id>/', views.display_receipt, name='display_receipt'),



]
