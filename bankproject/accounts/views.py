from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Account

@login_required
def account_list(request):
    accounts = Account.objects.filter(user=request.user)
    return render(request, 'accounts/account_list.html', {'accounts': accounts})

@login_required
def account_detail(request, account_id):
    account = Account.objects.get(id=account_id, user=request.user)
    return render(request, 'accounts/account_detail.html', {'account': account})
