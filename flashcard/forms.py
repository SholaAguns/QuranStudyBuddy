from django import forms
from .models import FlashcardSet
from .services.flashcard_service_factory import FlashcardServiceFactory

class FlashcardSetUpdateForm(forms.ModelForm):

    class Meta:
        model = FlashcardSet
        fields = ('title',)


class FlashcardSetForm(forms.Form):

    class Meta:
        fields = ('amount', 'service_type', 'request_type', 'id_list', 'range_start', 'range_end')

    def __init__(self, *args, **kwargs):
        factory = FlashcardServiceFactory()
        service_types = factory.list_services()
        self.fields['type'] = forms.ChoiceField(
            choices=[(service, service) for service in service_types],
            label="Flashcard Service Type"
        )
        request_types = ['default','byIDs', 'byRange', 'byJuz', 'byCategory']
        self.fields['type'] = forms.ChoiceField(
            choices=[(request_type, request_type) for request_type in request_types],
            label="Request Type"
        )

