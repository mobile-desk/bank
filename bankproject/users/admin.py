from django.contrib import admin
from .models import CustomerProfile

@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'customer_type', 'customer_number', 'date_of_birth')
    search_fields = ('user__username', 'customer_number')
    list_filter = ('customer_type',)

