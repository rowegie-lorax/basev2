from django import forms
from user.models import User


class RegistrationForm(forms.Form):
    email = forms.EmailField(
        error_messages={'required': 'Email address is required!'})
    phone_number = forms.CharField(
        error_messages={'required': 'Phone number is required!'})
    password = forms.CharField()

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        email = cleaned_data.get('email')
        phone_number = cleaned_data.get('phone_number')

        user_email = User.objects.all().filter(email__iexact=email).count()
        user_phone = User.objects.all().filter(
            phone_number__iexact=phone_number).count()

        if user_email != 0:
            self.add_error(
                'email', 'The email address "%s" is already with an account. Please use another email.' % email)
        if user_phone != 0:
            self.add_error(
                'phone_number', 'The phone number "%s" is already with an account. Please use another phone number.' % phone_number)
