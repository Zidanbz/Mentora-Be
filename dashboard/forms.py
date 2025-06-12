# dashboard/forms.py
from django import forms

class UploadFileForm(forms.Form):
    file = forms.FileField(label="Pilih File Excel")