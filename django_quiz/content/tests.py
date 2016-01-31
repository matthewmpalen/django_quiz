# -*- coding: utf-8 -*-
# Django
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.utils import IntegrityError
from django.test import Client, TestCase

# Local
from .models import Answer, Lesson, Question, Quiz

###############################################################################
# Models
###############################################################################

#########
# Lesson
#########

class LessonTitleTestCase(TestCase):
    def setUp(self):
        self.title1 = None
        self.title2 = ''
        self.title3 = 'Batman'
        self.title4 = 'バットマン'

        self.body = 'Lesson body'

    def test_none_title(self):
        with self.assertRaises(IntegrityError):
            lesson = Lesson.objects.create(title=self.title1, body=self.body)

    def test_blank_title(self):
        lesson = Lesson.objects.create(title=self.title2, body=self.body)

    def test_valid_ascii_title(self):
        lesson = Lesson.objects.create(title=self.title3, body=self.body)
        self.assertEqual(lesson.title, self.title3)

    def test_unicode_title(self):
        lesson = Lesson.objects.create(title=self.title4, body=self.body)
        self.assertEqual(lesson.title, self.title4)

class LessonBodyTestCase(TestCase):
    def setUp(self):
        self.title = 'Lesson title'

        self.body1 = None
        self.body2 = ''
        self.body3 = 'Lesson body'
        self.body4 = '授業'

    def test_none_body(self):
        with self.assertRaises(IntegrityError):
            lesson = Lesson.objects.create(title=self.title, body=self.body1)

    def test_blank_body(self):
        lesson = Lesson.objects.create(title=self.title, body=self.body2)

    def test_valid_ascii_body(self):
        lesson = Lesson.objects.create(title=self.title, body=self.body3)
        self.assertEqual(lesson.body, self.body3)

    def test_unicode_body(self):
        lesson = Lesson.objects.create(title=self.title, body=self.body4)
        self.assertEqual(lesson.body, self.body4)

class LessonDuplicateTestCase(TestCase):
    def setUp(self):
        self.title = 'Lesson title'
        self.body = 'Lesson body'
        self.lesson = Lesson.objects.create(title=self.title, body=self.body)

    def test_duplicate_creation(self):
        with self.assertRaises(IntegrityError):
            lesson = Lesson.objects.create(title=self.title, body=self.body)

#######
# Quiz
#######

class QuizLessonTestCase(TestCase):
    def setUp(self):
        self.lesson1 = None

        self.lesson_title = 'Lesson title'
        self.lesson_body = 'Lesson body'
        self.lesson2 = Lesson.objects.create(title=self.lesson_title, 
            body=self.lesson_body)

        self.title = 'Quiz title'

    def test_none_lesson(self):
        with self.assertRaises(ValueError):
            quiz = Quiz.objects.create(lesson=self.lesson1, title=self.title)

    def test_valid_lesson(self):
        quiz = Quiz.objects.create(lesson=self.lesson2, title=self.title)
        self.assertEqual(quiz.lesson.title, self.lesson_title)
        self.assertEqual(quiz.lesson.body, self.lesson_body)
        self.assertEqual(quiz.title, self.title)

class QuizTitleTestCase(TestCase):
    def setUp(self):
        self.lesson = Lesson.objects.create(title='Lesson title', 
            body='Lesson body')

        self.title1 = None
        self.title2 = ''
        self.title3 = 'Batman'
        self.title4 = 'バットマン'

    def test_none_title(self):
        with self.assertRaises(IntegrityError):
            quiz = Quiz.objects.create(lesson=self.lesson, title=self.title1)

    def test_blank_title(self):
        quiz = Quiz.objects.create(lesson=self.lesson, title=self.title2)

    def test_valid_ascii_title(self):
        quiz = Quiz.objects.create(lesson=self.lesson, title=self.title3)
        self.assertEqual(quiz.title, self.title3)

    def test_unicode_title(self):
        quiz = Quiz.objects.create(lesson=self.lesson, title=self.title4)
        self.assertEqual(quiz.title, self.title4)

class QuizDuplicateTestCase(TestCase):
    def setUp(self):
        self.lesson = Lesson.objects.create(title='Lesson title', 
            body='Lesson body')
        self.title = 'Quiz title'
        self.quiz = Quiz.objects.create(lesson=self.lesson, title=self.title)

    def test_duplicate_creation(self):
        with self.assertRaises(IntegrityError):
            quiz = Quiz.objects.create(lesson=self.lesson, title=self.title)

###########
# Question
###########

class QuestionQuizTestCase(TestCase):
    def setUp(self):
        self.quiz1 = None
        lesson = Lesson.objects.create(title='Lesson title', 
            body='Lesson body')
        self.quiz_title = 'Quiz title'
        self.quiz2 = Quiz.objects.create(lesson=lesson, title=self.quiz_title)

        self.body = 'Question body'

    def test_none_quiz(self):
        with self.assertRaises(ValueError):
            question = Question.objects.create(quiz=self.quiz1, body=self.body) 

    def test_valid_quiz(self):
        question = Question.objects.create(quiz=self.quiz2, body=self.body)
        self.assertEqual(question.quiz.title, self.quiz_title)
        self.assertEqual(question.body, self.body)

class QuestionBodyTestCase(TestCase):
    def setUp(self):
        lesson = Lesson.objects.create(title='Lesson title', 
            body='Lesson body')
        self.quiz = Quiz.objects.create(lesson=lesson, title='Quiz title')

        self.body1 = None
        self.body2 = ''
        self.body3 = 'Lesson body'
        self.body4 = '授業'

    def test_none_body(self):
        with self.assertRaises(IntegrityError):
            question = Question.objects.create(quiz=self.quiz, body=self.body1)

    def test_blank_body(self):
        question = Question.objects.create(quiz=self.quiz, body=self.body2)

    def test_valid_ascii_body(self):
        question = Question.objects.create(quiz=self.quiz, body=self.body3)
        self.assertEqual(question.body, self.body3)

    def test_unicode_body(self):
        question = Question.objects.create(quiz=self.quiz, body=self.body4)
        self.assertEqual(question.body, self.body4)

class QuestionCorrectAnswerTestCase(TestCase):
    def setUp(self):
        lesson = Lesson.objects.create(title='Lesson title', 
            body='Lesson body')
        self.quiz = Quiz.objects.create(lesson=lesson, title='Quiz title')

    def test_true_correct_answer(self):
        question = Question.objects.create(quiz=self.quiz, 
            body='Question body', correct_answer=True)
        self.assertTrue(question.correct_answer)

    def test_false_correct_answer(self):
        question = Question.objects.create(quiz=self.quiz, 
            body='Question body', correct_answer=False)
        self.assertFalse(question.correct_answer)

    def test_default_correct_answer(self):
        question = Question.objects.create(quiz=self.quiz, 
            body='Question body')
        self.assertFalse(question.correct_answer)

class QuestionDuplicateTestCase(TestCase):
    def setUp(self):
        self.lesson = Lesson.objects.create(title='Lesson title', 
            body='Lesson body')

        self.quiz = Quiz.objects.create(lesson=self.lesson, title='Quiz title')

        self.body = 'Question body'
        self.question = Question.objects.create(quiz=self.quiz, body=self.body)

    def test_duplicate_creation(self):
        with self.assertRaises(IntegrityError):
            question = Question.objects.create(quiz=self.quiz, body=self.body)

#########
# Answer
#########

class AnswerUserTestCase(TestCase):
    def setUp(self):
        self.user1 = None
        self.user_username = 'testuser'
        self.user2 = User.objects.create(username=self.user_username)
        
        self.lesson_title = 'Lesson title'
        self.lesson_body = 'Lesson body'
        self.lesson = Lesson.objects.create(title=self.lesson_title, 
            body=self.lesson_body)

        self.quiz_title = 'Quiz title'
        self.quiz = Quiz.objects.create(lesson=self.lesson, 
            title=self.quiz_title)

        self.question_body = 'Question body'
        self.question = Question.objects.create(quiz=self.quiz, 
            body=self.question_body)

        self.choice = False

    def test_none_user(self):
        with self.assertRaises(ValueError):
            answer = Answer.objects.create(user=self.user1, 
                question=self.question, choice=self.choice)

    def test_valid_user(self):
        answer = Answer.objects.create(user=self.user2, question=self.question, 
            choice=self.choice)
        self.assertEqual(answer.user, self.user2)
        self.assertEqual(answer.question, self.question)
        self.assertEqual(answer.choice, self.choice)
        self.assertTrue(answer.is_correct)

class AnswerQuestionTestCase(TestCase):
    def setUp(self):
        self.user_username = 'testuser'
        self.user = User.objects.create(username=self.user_username)
        
        self.lesson_title = 'Lesson title'
        self.lesson_body = 'Lesson body'
        self.lesson = Lesson.objects.create(title=self.lesson_title, 
            body=self.lesson_body)

        self.quiz_title = 'Quiz title'
        self.quiz = Quiz.objects.create(lesson=self.lesson, 
            title=self.quiz_title)

        self.question1 = None
        self.question_body = 'Question body'
        self.question2 = Question.objects.create(quiz=self.quiz, 
            body=self.question_body)

        self.choice = False

    def test_none_question(self):
        with self.assertRaises(ValueError):
            answer = Answer.objects.create(user=self.user, 
                question=self.question1, choice=self.choice)

    def test_valid_question(self):
        answer = Answer.objects.create(user=self.user, question=self.question2, 
            choice=self.choice)
        self.assertEqual(answer.user, self.user)
        self.assertEqual(answer.question, self.question2)
        self.assertEqual(answer.choice, self.choice)
        self.assertTrue(answer.is_correct)

class AnswerChoiceTestCase(TestCase):
    def setUp(self):
        self.user_username = 'testuser'
        self.user = User.objects.create(username=self.user_username)
        
        self.lesson_title = 'Lesson title'
        self.lesson_body = 'Lesson body'
        self.lesson = Lesson.objects.create(title=self.lesson_title, 
            body=self.lesson_body)

        self.quiz_title = 'Quiz title'
        self.quiz = Quiz.objects.create(lesson=self.lesson, 
            title=self.quiz_title)

        self.question_body = 'Question body'
        self.question = Question.objects.create(quiz=self.quiz, 
            body=self.question_body)

        self.choice1 = False
        self.choice2 = True

    def test_false_choice(self):
        answer = Answer.objects.create(user=self.user, question=self.question, 
            choice=self.choice1)
        self.assertEqual(answer.user, self.user)
        self.assertEqual(answer.question, self.question)
        self.assertEqual(answer.choice, self.choice1)
        self.assertTrue(answer.is_correct)

    def test_true_choice(self):
        answer = Answer.objects.create(user=self.user, question=self.question, 
            choice=self.choice2)
        self.assertEqual(answer.user, self.user)
        self.assertEqual(answer.question, self.question)
        self.assertEqual(answer.choice, self.choice2)
        self.assertFalse(answer.is_correct)

class AnswerDuplicateTestCase(TestCase):
    def setUp(self):
        self.user_username = 'testuser'
        self.user = User.objects.create(username=self.user_username)
        
        self.lesson_title = 'Lesson title'
        self.lesson_body = 'Lesson body'
        self.lesson = Lesson.objects.create(title=self.lesson_title, 
            body=self.lesson_body)

        self.quiz_title = 'Quiz title'
        self.quiz = Quiz.objects.create(lesson=self.lesson, 
            title=self.quiz_title)

        self.question_body = 'Question body'
        self.question = Question.objects.create(quiz=self.quiz, 
            body=self.question_body)

        self.answer = Answer.objects.create(user=self.user, 
            question=self.question)

    def test_duplicate_creation(self):
        with self.assertRaises(IntegrityError):
            answer = Answer.objects.create(user=self.user, 
                question=self.question)

###############################################################################
# Views
###############################################################################

#########
# Lesson
#########

class LessonListViewTestCase(TestCase):
    def setUp(self):
        self.url = reverse('lesson_list')
        self.client = Client()

        self.lesson1 = Lesson.objects.create(title='Music', 
            body='You must practice.')
        self.lesson2 = Lesson.objects.create(title='Strength Training', 
            body='1-5 reps.')

        self.username = 'testuser'
        self.password = '0xdeadbeef'
        self.user = User.objects.create_user(username=self.username, 
            password=self.password)

    def test_anonymous_user(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_authenticated_user(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        object_list = response.context['object_list']

        self.assertTrue(self.lesson1 in object_list)
        self.assertTrue(self.lesson2 in object_list)

class LessonDetailViewTestCase(TestCase):
    def setUp(self):
        self.lesson = Lesson.objects.create(title='Music', 
            body='You must practice.')

        self.url = reverse('lesson_detail', args=(self.lesson.id,))
        self.client = Client()

        self.username = 'testuser'
        self.password = '0xdeadbeef'
        self.user = User.objects.create_user(username=self.username, 
            password=self.password)

    def test_anonymous_user(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_authenticated_user(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        obj = response.context['object']

        self.assertTrue(self.lesson == obj)

#######
# Quiz
#######

class QuizDetailViewTestCase(TestCase):
    def setUp(self):
        self.lesson = Lesson.objects.create(title='Music', 
            body='You must practice.')
        self.quiz = Quiz.objects.create(lesson=self.lesson, title='Quiz title')

        self.url = reverse('quiz_detail', args=(self.quiz.id,))
        self.client = Client()

        self.username = 'testuser'
        self.password = '0xdeadbeef'
        self.user = User.objects.create_user(username=self.username, 
            password=self.password)

    def test_anonymous_user(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_authenticated_user(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        obj = response.context['object']

        self.assertTrue(self.quiz == obj)

class QuizAnswerListViewTestCase(TestCase):
    def setUp(self):
        self.lesson = Lesson.objects.create(title='Music', 
            body='You must practice.')
        self.quiz = Quiz.objects.create(lesson=self.lesson, title='Quiz title')
        self.question = Question.objects.create(quiz=self.quiz, 
            body='Question body')

        self.url = reverse('quiz_answer_list', args=(self.quiz.id,))
        self.client = Client()

        self.username1 = 'testuser'
        self.password1 = '0xdeadbeef'

        self.user1 = User.objects.create_user(username=self.username1, 
            password=self.password1)
        self.answer1 = Answer.objects.create(user=self.user1, 
            question=self.question)

        self.username2 = 'altuser'
        self.password2 = '0xbeefdead'

        self.user2 = User.objects.create_user(username=self.username2, 
            password=self.password2)
        self.answer2 = Answer.objects.create(user=self.user2, 
            question=self.question)

    def test_anonymous_user(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_authenticated_user(self):
        self.client.login(username=self.username1, password=self.password1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        object_list = response.context['object_list']

        # Only authenticated user's answers are served
        self.assertTrue(self.answer1 in object_list)
        self.assertTrue(self.answer2 not in object_list)

###########
# Question
###########

class QuestionDetailViewTestCase(TestCase):
    def setUp(self):
        self.lesson = Lesson.objects.create(title='Music', 
            body='You must practice.')
        self.quiz = Quiz.objects.create(lesson=self.lesson, title='Quiz title')
        self.question = Question.objects.create(quiz=self.quiz, 
            body='Question body')

        self.url = reverse('question_detail', args=(self.question.id,))
        self.client = Client()

        self.username = 'testuser'
        self.password = '0xdeadbeef'
        self.user = User.objects.create_user(username=self.username, 
            password=self.password)

    def test_anonymous_user(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_authenticated_user(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        obj = response.context['object']

        self.assertTrue(self.question == obj)

#########
# Answer
#########

class AnswerCreateViewTestCase(TestCase):
    def setUp(self):
        self.lesson = Lesson.objects.create(title='Music', 
            body='You must practice.')
        self.quiz = Quiz.objects.create(lesson=self.lesson, title='Quiz title')
        self.question = Question.objects.create(quiz=self.quiz, 
            body='Question body')

        self.url = reverse('answer_create', args=(self.question.id,))
        self.client = Client()

        self.username = 'testuser'
        self.password = '0xdeadbeef'
        self.user = User.objects.create_user(username=self.username, 
            password=self.password)

    def test_anonymous_user(self):
        data = {'choice': False}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)

    def test_authenticated_user(self):
        self.client.login(username=self.username, password=self.password)
        data = {'choice': False}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        url = reverse('lesson_list')
        self.assertEqual(response['Location'], url)
