from django import forms
from .models import Phrase

class PhraseForm(forms.ModelForm):

    class Meta:
        model = Phrase
        fields = ('text', 'translation', 'category', 'tags', 'image')

    def __init__(self, *args, **kwargs):
        super(PhraseForm, self).__init__(*args, **kwargs)
        self.fields['image'].required = False
        self.fields['tags'].required = False
        self.fields['category'].required = False