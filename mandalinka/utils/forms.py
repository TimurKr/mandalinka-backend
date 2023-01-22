from django.urls import reverse

from crispy_forms.layout import BaseInput
from crispy_forms.bootstrap import StrictButton


class SubmitButton(BaseInput):
    """Custom submit button."""""
    input_type = 'submit'
    field_classes = 'btn primary-button'

class SecondarySubmitButton(BaseInput):
    """Custom secondary submit button"""
    input_type = 'submit'
    field_classes = 'btn secondary-button'

class SecondaryButton(StrictButton):
    """Custom secondary button
    
    takes extra argument on init:
    - onclick: the url to redirect to on click, only the 'app:name'
    """
    field_classes = 'btn secondary-button'

    def __init__(self, content, onclick = None, *args, **kwargs):
        if onclick:
            onclick = f'location.href="{reverse(onclick)}"'
            super().__init__(content, onclick=onclick, *args, **kwargs)
        else:
            super().__init__(content, *args, **kwargs)
