from django.db import models
from django.contrib.auth.models import User

class ItemCategory(models.Model):
    name = models.CharField(max_length=225)
    slug = models.SlugField(max_length=450)

class Item(models.Model):
    name = models.CharField(max_length=150)

class CharacterClass(models.Model):
    name = models.CharField(max_length=150)

class Character(models.Model):
    name = model.CharField(max_length=150)
