# -*- coding: utf-8 -*-
# Django
from django.db.utils import IntegrityError
from django.test import TestCase

# Local
from .models import Tag

######
# Tag
######

class TagNameTestCase(TestCase):
    def setUp(self):
        self.name1 = None
        self.name2 = ''
        self.name3 = 'music'
        self.name4 = 'タッグ'

    def test_none_name(self):
        with self.assertRaises(IntegrityError):
            tag = Tag.objects.create(name=self.name1)

    def test_blank_name(self):
        tag = Tag.objects.create(name=self.name2)
        self.assertEqual(tag.name, self.name2)

    def test_valid_ascii_name(self):
        tag = Tag.objects.create(name=self.name3)
        self.assertEqual(tag.name, self.name3)

    def test_unicode_name(self):
        tag = Tag.objects.create(name=self.name4)
        self.assertEqual(tag.name, self.name4)

class TagDuplicateTestCase(TestCase):
    def setUp(self):
        self.name = 'music'
        self.tag = Tag.objects.create(name=self.name)

    def test_duplicate_creation(self):
        with self.assertRaises(IntegrityError):
            tag = Tag.objects.create(name=self.name)
