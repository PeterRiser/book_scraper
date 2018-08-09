# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db.models import Sum

# Create your models here.


class Category(models.Model):
    name = models.CharField(blank=False, max_length=32, unique=True)
    url = models.CharField(blank=False, max_length=64, default='')

    def __str__(self):
        return self.name.encode('utf-8')

    def count_books(self):
        val = Book.objects.filter(category=self.id)
        return len(val)

    def average_price(self):
        val = Book.objects.filter(category=self.id)
        return round(val.aggregate(Sum('price'))['price__sum'] / len(val), 2)


class Book(models.Model):
    upc = models.CharField(unique=True, max_length=64)
    title = models.CharField(blank=False, max_length=32)
    rating = models.IntegerField(blank=False)
    category = models.ForeignKey(Category)
    in_stock = models.IntegerField(blank=False)
    price = models.FloatField(blank=False)
    reviews = models.IntegerField(blank=False)

    def __str__(self):
        return self.title.encode('utf-8')
