from django.contrib import admin
from .models import Transaction,Beneficiary,ScheduledPayment, Receipt

admin.site.register(Transaction)
admin.site.register(Beneficiary)
admin.site.register(ScheduledPayment)
admin.site.register(Receipt)
