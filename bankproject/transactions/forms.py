from django import forms
from accounts.models import Account
from django.utils import timezone

class PaymentForm(forms.Form):
    from_account = forms.ModelChoiceField(queryset=None)
    to_account = forms.CharField()
    amount = forms.DecimalField(max_digits=10, decimal_places=2)
    pay_now = forms.BooleanField(required=False, initial=True)
    payment_date = forms.DateTimeField(required=False, widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    save_beneficiary = forms.BooleanField(required=False)
    beneficiary_name = forms.CharField(required=False)

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['from_account'].queryset = Account.objects.filter(user=user)

    def clean(self):
        cleaned_data = super().clean()
        pay_now = cleaned_data.get('pay_now')
        payment_date = cleaned_data.get('payment_date')

        if not pay_now and not payment_date:
            raise forms.ValidationError("Please select a payment date for future payments.")

        if not pay_now and payment_date and payment_date <= timezone.now():
            raise forms.ValidationError("Future payment date must be in the future.")

        return cleaned_data

