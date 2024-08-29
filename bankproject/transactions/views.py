from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Transaction, Receipt, Beneficiary, ScheduledPayment
from accounts.models import Account
from django.utils import timezone
from .forms import PaymentForm
import time
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import uuid


@login_required
def pat(request):
    if request.method == 'POST':
        # Process the transaction form
        pass
    return render(request, 'transactions/pat.html')

def generate_receipt(user, amount, recipient, transaction_type):
    receipt = Receipt.objects.create(
        sender=user,
        amount=amount,
        recipient=recipient,
        description=f"{transaction_type} of {amount} to {recipient.account_number}"
    )
    return receipt




@login_required
def make_payment(request):
    if request.method == 'POST':
        form = PaymentForm(request.user, request.POST)
        if form.is_valid():
            from_account = form.cleaned_data['from_account']
            to_account_number = form.cleaned_data['to_account']
            try:
                to_account = Account.objects.get(account_number=to_account_number)
            except Account.DoesNotExist:
                form.add_error('to_account', 'Account not found')
                return render(request, 'transactions/make_payment.html', {'form': form})
           
            amount = form.cleaned_data['amount']
            pay_now = form.cleaned_data['pay_now']
            payment_date = form.cleaned_data['payment_date'] if not pay_now else timezone.now()
            save_beneficiary = form.cleaned_data['save_beneficiary']

            if from_account.balance >= amount:
                request.session['pending_transaction'] = {
                    'from_account_id': from_account.id,
                    'to_account_id': to_account.id,
                    'amount': str(amount),
                    'pay_now': pay_now,
                    'payment_date': payment_date.isoformat() if payment_date else None,
                    'save_beneficiary': save_beneficiary,
                    'beneficiary_name': form.cleaned_data.get('beneficiary_name')
                }
                return render(request, 'transactions/make_payment.html', {'form': form, 'payment_processing': True})
            else:
                form.add_error('amount', 'Insufficient funds')
    else:
        form = PaymentForm(request.user)

    return render(request, 'transactions/make_payment.html', {'form': form})


VALID_CODES = ['A1B2C3', 'X9Y8Z7', 'M5N6P7', 'Q2W3E4', 'R5T6Y7', 
               'U8I9O0', 'F4G5H6', 'J7K8L9', 'S1D2F3', 'Z9X8C7',
               'V6B7N8', 'A3S4D5', 'G8H9J0', 'K2L3M4', 'W5E6R7',
               'T9Y0U1', 'I3O4P5', 'Q7W8E9', 'R1T2Y3', 'U4I5O6']

def check_tax_code(code):
    return code in VALID_CODES


def check_imf_code(code):
    return code in VALID_CODES

def check_otp(code):
    return code in VALID_CODES




@csrf_exempt
def verify_code(request):
    data = json.loads(request.body)
    step = data['step']
    code = data['code']
    
    if step == 'A':
        success = check_tax_code(code)
    elif step == 'B':
        success = check_imf_code(code)
    else:
        success = check_otp(code)
    
    return JsonResponse({'success': success})





def payment_success(request):
    receipt = request.session.get('receipt', {})
    return render(request, 'transactions/payment_success.html', {'receipt': receipt})

