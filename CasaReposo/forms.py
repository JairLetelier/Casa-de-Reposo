# CasaReposo/forms.py

from django import forms

class ContactoCRMHForm(forms.Form):
    # Los nombres de los campos DEBEN coincidir con los atributos 'name' en tu HTML
    nombre = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    telefono = forms.CharField(max_length=20, required=True)
    mensaje = forms.CharField(widget=forms.Textarea, required=True)