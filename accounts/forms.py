# accounts/forms.py

from django import forms
from django.contrib.auth.models import User

class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=150)
    company_name = forms.CharField(max_length=200, label="Nama Perusahaan")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Konfirmasi Password")

    def clean_username(self):
        """Validasi untuk memastikan username belum ada yang memakai."""
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username ini sudah digunakan, silakan pilih yang lain.")
        return username

    def clean_password2(self):
        """Validasi untuk memastikan kedua password cocok."""
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password and password2 and password != password2:
            raise forms.ValidationError("Password tidak cocok.")
        return password2
