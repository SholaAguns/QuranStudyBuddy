from django import forms
from .models import Scorecard

from django.contrib.auth import get_user_model
User = get_user_model()

class ScorecardManualCreationForm(forms.ModelForm):
    user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label="Select User",
        empty_label="Choose a user",
        widget=forms.Select(attrs={'class': 'form-control'}),  # Optional styling
    )

    class Meta:
        model = Scorecard
        fields = ['user',]


class ScorecardUpdateForm(forms.Form):
    user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"}),
        label="Select User",
    )