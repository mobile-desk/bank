from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Transaction, PendingTransaction, Receipt, Beneficiary, ScheduledPayment
from accounts.models import Account
from django.utils import timezone
from .forms import PaymentForm
import time
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import uuid
from decimal import Decimal





@login_required
def pat(request):
    if request.method == 'POST':
        # Process the transaction form
        pass
    return render(request, 'transactions/pat.html')



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




'''@csrf_exempt
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
'''



@login_required
def transaction_list(request):
    # Assuming the user has multiple accounts and you want to get transactions for all of them
    accounts = Account.objects.filter(user=request.user)
    transactions = Transaction.objects.filter(account__in=accounts).order_by('-timestamp')
    return render(request, 'transactions/transaction_list.html', {'transactions': transactions})


@login_required
def make_payment(request):
    if request.method == 'POST':
        form = PaymentForm(request.user, request.POST)
        if form.is_valid():
            from_account = form.cleaned_data['from_account']
            to_account = Account.objects.get(account_number=form.cleaned_data['to_account'])
            amount = form.cleaned_data['amount']
            
            if from_account.balance >= amount:
                recipient_name = f"{to_account.user.first_name} {to_account.user.last_name}"
                receipt = Receipt.objects.create(
                    sender=request.user,
                    amount=amount,
                    recipient=to_account,
                    description=f"Transfer to {to_account.account_number} - {recipient_name}"
                )


                PendingTransaction.objects.create(
                    user=request.user,
                    from_account_id=from_account.id,
                    to_account_id=to_account.id,
                    amount=amount,
                    pay_now=form.cleaned_data['pay_now'],
                    payment_date=form.cleaned_data['payment_date'],
                    save_beneficiary=form.cleaned_data['save_beneficiary'],
                    beneficiary_name=form.cleaned_data.get('beneficiary_name'),
                    receipt_id=str(receipt.id)
                )
                
                
                return render(request, 'transactions/verification.html')
            else:
                form.add_error('amount', 'Insufficient funds')
    else:
        form = PaymentForm(request.user)
    
    return render(request, 'transactions/make_payment.html', {'form': form})





@csrf_exempt
def verify_transaction(request):
    data = json.loads(request.body)
    step = data['step']
    code = data['code']
    
    if step == 'A':
        success = check_tax_code(code)
    elif step == 'B':
        success = check_imf_code(code)
    else:
        success = check_otp(code)
    
    if step == 'C' and success:
        pending_transaction = PendingTransaction.objects.filter(user=request.user).latest('created_at')
        from_account = Account.objects.get(id=pending_transaction.from_account_id)
        to_account = Account.objects.get(id=pending_transaction.to_account_id)
        amount = pending_transaction.amount
        
        from_account.balance -= amount
        from_account.save()
        
        to_account.balance += amount
        to_account.save()
        
        Transaction.objects.create(
            account=from_account,
            amount=-amount,
            transaction_type='Debit',
            description=f'Transfer to {to_account.account_number}'
        )
        
        Transaction.objects.create(
            account=to_account,
            amount=amount,
            transaction_type='Credit',
            description=f'Received from {from_account.account_number}'
        )
        
        receipt = Receipt.objects.get(id=pending_transaction.receipt_id)
        receipt.save()
        
        pending_transaction.delete()
        
        return JsonResponse({'success': True, 'receipt_id': str(receipt.id)})
    
    return JsonResponse({'success': success})





def display_receipt(request, receipt_id):
    receipt = Receipt.objects.get(id=receipt_id)
    return render(request, 'transactions/receipt.html', {'receipt': receipt})
