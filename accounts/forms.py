from django import forms
from django.contrib.auth.forms import PasswordChangeForm


class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    
class PasswordChangingForm(PasswordChangeForm):
    old_password = forms.CharField(label="Old Password", strip=False, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password1 = forms.CharField(label="New Password", strip=False, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = forms.CharField(label="Confirm New Password", strip=False, widget=forms.PasswordInput(attrs={'class': 'form-control'}))