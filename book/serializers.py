# -*- coding: utf-8 -*-

from django.core.exceptions import ObjectDoesNotExist

import models
from models import Category
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class BookSerializer:
    """all validators below effectively do the same thing. they take the data. clean it to be correct type"""

    def validate(self, data):
        # validation function to call all other validators
        valid_data = {}
        valid_data['upc'] = self.validate_upc(data['upc'])
        valid_data['title'] = self.validate_title(data['title'])
        valid_data['rating'] = self.validate_rating(data['rating'])
        valid_data['category'] = self.validate_category(data['category'])
        valid_data['in_stock'] = self.validate_in_stock(data['in_stock'])
        valid_data['price'] = self.validate_price(data['price'])
        valid_data['reviews'] = self.validate_reviews(data['reviews'])
        return valid_data

    def validate_upc(self, value):
        try:
            ret = value.replace('\n', '').lower().lstrip().rstrip()
            return ret
        except Exception as e:
            raise ValidationError('The UPC is invalid because {}'.format(e))

    def validate_title(self, value):
        try:
            ret = value.replace(u"\u2018", "'").replace(u"\u2019", "'").replace('\n', '').lower().lstrip().rstrip()
            return ret
        except Exception as e:
            print(value)
            print(e)
            raise ValidationError('The title is invalid because {}'.format(e))

    def validate_rating(self, value):
        try:
            value = value.lower()
            word_to_int = {'zero': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5}
            if value in word_to_int.keys():
                return word_to_int[value]
            else:
                raise ValidationError('rating was invalid value')
        except Exception as e:
            print(e)
            raise ValidationError('The rating is invalid because {}'.format(e))

    def validate_category(self, value):
        try:
            # because this is a foriegn key, we check if the category exists
            ret = Category.objects.get(name=value.encode())
            return ret
        except ObjectDoesNotExist as e:
            raise ValidationError("Category does not exist")
        except Exception as e:
            print(e)
            raise ValidationError('The category is invalid because {}'.format(e))

    def validate_in_stock(self, value):
        try:
            ret = int(value.split(' ')[2][1:])
            return ret
        except Exception as e:
            print(e)
            raise ValidationError('The stock value is invalid because {}'.format(e))

    def validate_price(self, value):
        try:
            return float(value[1:])
        except Exception as e:
            print(e)
            raise ValidationError('The price value is invalid because {}'.format(e))

    def validate_reviews(self, value):
        try:
            return int(value)
        except Exception as e:
            print(e)
            raise ValidationError('The reviews value is invalid because {}'.format(e))
