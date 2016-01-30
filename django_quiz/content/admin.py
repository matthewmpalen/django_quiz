# Django
from django.contrib import admin

# Local
from .models import Lesson, Quiz, Question, Answer

class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'body', 'created_at', 'updated_at')

class QuizAdmin(admin.ModelAdmin):
    list_display = ('lesson', 'title', 'created_at', 'updated_at')
    list_filter = ('lesson',)

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('quiz', 'body', 'correct_answer', 'created_at', 
        'updated_at')
    list_filter = ('quiz', 'quiz__lesson')

class AnswerAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'choice', 'is_correct', 'created_at', 
        'updated_at')
    list_filter = ('user', 'is_correct', 'question__quiz')

admin.site.register(Lesson, LessonAdmin)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
