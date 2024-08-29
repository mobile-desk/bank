from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CustomerTypeForm(forms.Form):
    CUSTOMER_TYPES = [
        ('personal', 'Personal or Premier'),
        ('business', 'Business'),
        ('credit_card', 'Credit Card Only'),
        ('mortgage', 'Mortgage Only'),
    ]
    customer_type = forms.ChoiceField(choices=CUSTOMER_TYPES, widget=forms.RadioSelect)

class PersonalCustomerForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    middle_name = forms.CharField(max_length=100, required=False)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    postcode = forms.CharField(max_length=10, required=False)

class BusinessCustomerForm(PersonalCustomerForm):
    business_postcode = forms.CharField(max_length=10)

class CreditCardCustomerForm(PersonalCustomerForm):
    pass

class MortgageCustomerForm(PersonalCustomerForm):
    pass

class AccountSetupForm(forms.Form):
    customer_number = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    saved_number = forms.BooleanField(required=True)
    KNOW_PIN_CHOICES = [
        ('yes', 'I know my PIN and password'),
        ('no', 'I don\'t know my PIN'),
    ]
    know_pin = forms.ChoiceField(choices=KNOW_PIN_CHOICES, widget=forms.RadioSelect)

class PinPasswordForm(forms.Form):
    pin = forms.CharField(max_length=4, widget=forms.PasswordInput)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

'''
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
'''