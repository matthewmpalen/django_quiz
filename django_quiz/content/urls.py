# Django
from django.conf.urls import url

# Local
from .views import AnswerCreateView, LessonDetailView, LessonListView 
from .views import QuestionDetailView, QuizAnswerListView, QuizDetailView

urlpatterns = [
    url(r'^lesson/$', LessonListView.as_view(), name='lesson_list'), 
    url(r'^lesson/(?P<pk>\d+)/$', LessonDetailView.as_view(), 
        name='lesson_detail'), 
    url(r'^quiz/(?P<pk>\d+)/$', QuizDetailView.as_view(), name='quiz_detail'), 
    url(r'^quiz/(?P<pk>\d+)/answer/$', QuizAnswerListView.as_view(), 
        name='quiz_answer_list'), 
    url(r'^question/(?P<pk>\d+)/$', QuestionDetailView.as_view(), 
        name='question_detail'), 
    url(r'^question/(?P<pk>\d+)/answer/create/$', AnswerCreateView.as_view(), 
        name='answer_create')
]
