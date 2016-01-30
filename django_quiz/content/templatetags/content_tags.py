# Django
from django import template
from django.core.exceptions import ObjectDoesNotExist

# Local
from django_quiz.content.models import Answer

register = template.Library()

@register.inclusion_tag('content/answers/templatetags/get_user_answer.html')
def get_user_answer(question, user):
    context = {
        'user_answer': None, 
    }

    if not question:
        return context

    if not user:
        return context

    user_answer = None
    try:
        user_answer = Answer.objects.get(question=question, user=user)
    except ObjectDoesNotExist as e:
        return context

    context = {
        'user_answer': user_answer
    }

    return context
