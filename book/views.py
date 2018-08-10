# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

import django_tables2 as tables
import tasks
from django_tables2 import Column, RequestConfig
from django_tables2.utils import A
from models import Book, Category

# Create your views here.


class BookTable(tables.Table):
    """masks the db table out to a html table"""
    class Meta:
        model = Book
        template_name = 'django_tables2/bootstrap.html'


class CategoryTable(tables.Table):
    """masks the db table out to a html table and calls the functions to count and average the book data"""
    number_of_books = Column(accessor=A('count_books'),
                             verbose_name='# of Books')
    avg = Column(accessor=A('average_price'),
                 verbose_name='average price')

    class Meta:
        model = Category
        fields = ['id', 'name']
        sequence = ('id', 'name', 'number_of_books')


def index(request):
    """this is the homepage view in the application"""
    # initializes books table
    books = BookTable(Book.objects.all())
    RequestConfig(request).configure(books)
    categories = CategoryTable(Category.objects.all())
    # sets book pagination
    books.paginate(page=request.GET.get('page', 1), per_page=20)
    # calculates philosphy avg price
    phil = Category.objects.get(name='philosophy').average_price()
    return render(request=request, template_name='index.html', context={'categories': categories, 'books': books, 'phil': phil})
