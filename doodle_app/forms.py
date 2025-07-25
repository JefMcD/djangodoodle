import re
from django import forms
from django.core.exceptions import ValidationError
from .models import *

# utils/validators.py (or forms.py if you prefer)
def validate_password_strength(password):
    if len(password) < 8:
        raise ValidationError("Password must be at least 8 characters long.")
    if not re.search(r'[A-Z]', password):
        raise ValidationError("Password must contain at least one uppercase letter.")
    if not re.search(r'[a-z]', password):
        raise ValidationError("Password must contain at least one lowercase letter.")
    if not re.search(r'\d', password):
        raise ValidationError("Password must contain at least one number.")
    #if not re.search(r'[^\w\s]', password):  # special character
    #    raise ValidationError("Password must contain at least one special character.")

    
def is_disposable_email(email):
    domain = email.split('@')[-1].lower()
    disposable_domains = set([
        "mailinator.com", "10minutemail.com", "tempmail.io",
        "guerrillamail.com", "yopmail.com"
        # or load this list from a file
    ])
    return domain in disposable_domains

 

class SignInForm(forms.Form):
    username    = forms.CharField(
        label="",
        max_length=16,
        widget=forms.TextInput(attrs={
        "class": "form-input",
        "name" : "username",
        "placeholder": "Username",
        "autofocus": True,
    }))
    password    = forms.CharField(
        label="",
        max_length=45,
        widget=forms.PasswordInput(attrs={
        "class": "form-input",
        "id"   : "signup-form-pass",
        "name" : "password",
        "placeholder": "Password",
    }))
    
    
    
    
    
    
    
    
class JoinForm(forms.Form):
    firstname    = forms.CharField(
        label="",
        max_length=16,
        widget=forms.TextInput(attrs={
        "class": "form-input",
        "name" : "firstname",
        "placeholder": "Firstname",
        "autofocus": True,
    }))
    lastname    = forms.CharField(
        label="",
        max_length=16,
        widget=forms.TextInput(attrs={
        "class": "form-input",
        "name" : "lastname",
        "placeholder": "Lastname",
    }))
    username    = forms.CharField(
        label="",
        max_length=16,
        widget=forms.TextInput(attrs={
        "class": "form-input",
        "name" : "username",
        "placeholder": "Username",
    }))
    email   = forms.EmailField(
        label="",
        max_length=45,
        widget=forms.TextInput(attrs={
        "class": "form-input",
        "name" : "email",
        "placeholder": "Email",
    }))
    password    = forms.CharField(
        label="",
        max_length=45,
        widget=forms.PasswordInput(attrs={
        "class" : "form-input",
        "id"    : "join-form-password",
        "name"  : "password",
        "placeholder": "Password",
    }))
    confirm    = forms.CharField(
        label="",
        min_length = 8,
        max_length=45,
        widget=forms.PasswordInput(attrs={
        "class": "form-input",
        "name" : "password",
        "placeholder": "Confirm Password",
    }))
    
    
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not email:
            return email  # Let Django's default 'required' handle this

        if is_disposable_email(email):
            raise ValidationError("High Ho Silver! Away!", code="blocked")
        return email
            
    def clean_password(self):
        password = self.cleaned_data.get("password")
        validate_password_strength(password)
        return password
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm = cleaned_data.get("confirm")

        if password and confirm and password != confirm:
            self.add_error("confirm", "Passwords do not match.") # associates error with confirm field
        
            
            
    
    
            
            
    

class PasswordResetForm(forms.Form):
    email   = forms.EmailField(
        label="",
        widget=forms.TextInput(attrs={
        "class": "form-input",
        "name" : "email",
        "placeholder": "Email",
        "autofocus": True,
    }))
    def clean_password(self):
        password = self.cleaned_data.get("password")
        validate_password_strength(password)
        return password
    
class CodeVerificationForm(forms.Form):
    verification_code = forms.IntegerField(
        label="",
        widget=forms.NumberInput(attrs={
            "class": "form-input",
            "name" : "verification_code",
            "placeholder": "Secret Code",
            "autofocus": True,
        })
    )
    
class pic_inputs(forms.Form):
    pass

class time_inputs(forms.Form):
    pass

class music_inputs(forms.Form):
    pass

