# Django
from django.core.urlresolvers import reverse
from django.views.generic import DetailView, CreateView, ListView

# Local
from .forms import AnswerForm
from .models import Answer, Lesson, Question, Quiz
from django_quiz.mixins import LoginRequiredMixin

class LessonListView(LoginRequiredMixin, ListView):
    model = Lesson
    template_name = 'content/lessons/list.html'

class LessonDetailView(LoginRequiredMixin, DetailView):
    model = Lesson
    template_name = 'content/lessons/detail.html'

class QuizDetailView(LoginRequiredMixin, DetailView):
    model = Quiz
    template_name = 'content/quizzes/detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        quiz = self.get_object()
        unanswered_questions = quiz.get_unanswered_questions(self.request.user)
        context['done'] = unanswered_questions.count() == 0
        return context

class QuizAnswerListView(LoginRequiredMixin, ListView):
    model = Answer
    template_name = 'content/quizzes/answers/list.html'

    def get_queryset(self):
        self.quiz = Quiz.objects.get(id=self.kwargs['pk'])
        return Answer.objects.filter(user=self.request.user, 
            question__quiz=self.quiz)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['score'] = self.quiz.get_score(self.request.user)
        return context

class QuestionDetailView(LoginRequiredMixin, DetailView):
    model = Question
    template_name = 'content/questions/detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        user_answer = self.get_object().get_user_answer(self.request.user)
        if user_answer:
            context['already_answered'] = True
        else:
            context['already_answered'] = False
            context['form'] = AnswerForm
        return context

class AnswerCreateView(LoginRequiredMixin, CreateView):
    model = Answer
    template = 'content/answers/create.html'
    form_class = AnswerForm

    def get_success_url(self):
        quiz = self.get_object().question.quiz
        questions = Question.objects.filter(quiz=quiz)
        for question in questions:
            if not question.get_user_answer(self.request.user):
                return question.get_absolute_url()

        return reverse('lesson_list')

    def form_valid(self, form):
        if form.is_valid():
            form.instance.user = self.request.user
            question = Question.objects.get(id=self.kwargs['pk'])
            form.instance.question = question

        return super().form_valid(form)
