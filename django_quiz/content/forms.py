# Django
from django.forms import ModelForm

# Local
from .models import Answer

class AnswerForm(ModelForm):
    class Meta:
        model = Answer
        fields = ('choice',)
