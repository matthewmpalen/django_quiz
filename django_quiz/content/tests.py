# -*- coding: utf-8 -*-
# Django
from django.db.utils import IntegrityError
from django.test import TestCase

# Local
from .models import Lesson, Question, Quiz

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
