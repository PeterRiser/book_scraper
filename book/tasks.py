# -*- coding: utf-8 -*-
import re
from urllib import urlopen
from urlparse import urlparse

import requests

from bs4 import BeautifulSoup
from models import Book, Category
from serializers import BookSerializer


def clean_html(string):

    return string.replace(u"\u2018", "'").replace(u"\u2019", "'").replace('\n', '').lower().lstrip().rstrip()


def scrape_categories():
    """this is to grab categories"""

    html = urlopen("http://books.toscrape.com/index.html")
    bsObj = BeautifulSoup(html.read(), features="html.parser")
    html = bsObj.findAll("div", {"class": "side_categories"})[0].findAll('li')[1:]
    for tag in html:
        name = clean_html(tag.text)
        if not Category.objects.filter(name=name).exists():
            new_cat = Category.objects.create(name=name, url=tag.findNext('a')['href'])

    return


def scrape_books():
    table_to_html = {'UPC': 'upc', 'Price (incl. tax)': 'price',
                     'Availability': 'in_stock', 'Number of reviews': 'reviews'}
    html = urlopen("http://books.toscrape.com/index.html")
    bsObj = BeautifulSoup(html.read(), features="html.parser")
    num_pages_text = bsObj.find('li', {"class": "current"})
    num_pages = clean_html(num_pages_text.text).split(' ')[-1]
    print("starting book scraping")
    for i in range(0, int(num_pages)):
        catalogue = requests.get("http://books.toscrape.com/catalogue/page-{}.html".format(i + 1))
        bs_book = BeautifulSoup(catalogue.text, features="html.parser")
        books = bs_book.findAll("article", {"class": "product_pod"})
        for book in books:
            kwargs = {}
            b = book.findNext('div', {'class': 'image_container'})
            book_url = b.findNext('a')['href']
            print("http://books.toscrape.com/" + book_url)
            book_object = BeautifulSoup(urlopen("http://books.toscrape.com/catalogue/" +
                                                book_url).read(), features="html.parser")
            kwargs['title'] = book_object.find('title').text.split('|')[0].rstrip().lstrip()
            kwargs['rating'] = book_object.find('p', class_=re.compile('star-rating'))['class'][1]
            category = clean_html(book_object.find('ul', {'class': "breadcrumb"}).findAll('li')[2].text)
            kwargs['category'] = category
            tbl = book_object.find('table', {'class': 'table table-striped'})
            for row in tbl.findAll('tr'):
                th = row.find('th')
                td = row.find('td')
                if th.text in table_to_html.keys():
                    kwargs[table_to_html[th.text]] = td.text

            serial_book = BookSerializer()
            data = serial_book.validate(kwargs)
            if Book.objects.filter(upc=data['upc']).exists():
                pass
            else:
                Book.objects.create(**data)
    return
