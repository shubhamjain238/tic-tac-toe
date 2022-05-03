from .models import Invitation
from django import forms
from django.contrib.auth.models import User
class Invitation_Form(forms.ModelForm):
    class Meta:
        model = Invitation
        exclude = ['from_user', 'timestamp']