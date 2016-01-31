# Django
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext as _

# Local
from django_quiz.common.models import Tag

class Lesson(models.Model):
    title = models.CharField(max_length=50, unique=True)
    body = models.TextField(max_length=2000)
    tags = models.ManyToManyField(Tag, related_name='%(class)s')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('lesson_detail', args=(self.id,))

class Quiz(models.Model):
    lesson = models.ForeignKey(Lesson)
    title = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (
            ('lesson', 'title')
        )
        verbose_name_plural = _('quizzes')

    def __str__(self):
        return '{0}: {1}'.format(self.lesson, self.title)

    def get_absolute_url(self):
        return reverse('quiz_detail', args=(self.id,))

    def get_unanswered_questions(self, user):
        user_answers = Answer.objects.filter(user=user)
        question_ids = [answer.question.id for answer in user_answers]
        return self.question_set.exclude(id__in=question_ids)

    def get_score(self, user):
        correct_answer_count = Answer.objects.filter(user=user, 
            question__quiz=self, is_correct=True).count()
        question_count = Question.objects.filter(quiz=self).count()
        if question_count == 0:
            return 'N/A'
        return '{0:.2%}'.format(correct_answer_count / question_count)


class Question(models.Model):
    quiz = models.ForeignKey(Quiz)
    body = models.TextField(max_length=1000)
    correct_answer = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (
            ('quiz', 'body')
        )

    def __str__(self):
        return self.body

    def get_user_answer(self, user):
        try:
            answer = self.answer_set.get(user=user, question=self)
        except ObjectDoesNotExist as e:
            answer = Answer.objects.none()

        return answer

class Answer(models.Model):
    user = models.ForeignKey(User)
    question = models.ForeignKey(Question)
    choice = models.BooleanField(default=False, 
        verbose_name='True or False?', help_text='Checked=True')
    is_correct = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (
            ('user', 'question')
        )

    def __str__(self):
        return '{0}'.format(self.choice)

    def save(self, *args, **kwargs):
        self.is_correct = self.choice == self.question.correct_answer
        super().save(*args, **kwargs)
