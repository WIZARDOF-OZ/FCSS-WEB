from django import forms
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from App.models import StudentApplication


class StudentRegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    father_name = forms.CharField(max_length=150)
    mother_name = forms.CharField(max_length=150)
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=15)
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    gender = forms.ChoiceField(choices=StudentApplication.GENDER_CHOICES)
    applying_class = forms.CharField(max_length=50)
    course = forms.CharField(max_length=20, required=False)

    password_choice = forms.ChoiceField(choices=StudentApplication.PASSWORD_CHOICE, initial='auto')
    custom_password = forms.CharField(required=False, widget=forms.PasswordInput)
    custom_password_confirm = forms.CharField(required=False, widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        from django.contrib.auth.models import User
        if User.objects.filter(username=email).exists():
            raise ValidationError('An account with this email already exists. Please log in instead.')
        return email

    def clean(self):
        cleaned = super().clean()
        choice = cleaned.get('password_choice')

        if choice == 'custom':
            pw1 = cleaned.get('custom_password')
            pw2 = cleaned.get('custom_password_confirm')

            if not pw1:
                raise ValidationError({'custom_password': 'Please enter a password.'})
            if pw1 != pw2:
                raise ValidationError({'custom_password_confirm': 'Passwords do not match.'})

            # Run Django's built-in password strength validators
            try:
                validate_password(pw1)
            except ValidationError as e:
                raise ValidationError({'custom_password': e.messages})

        return cleaned