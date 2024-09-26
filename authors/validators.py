from typing import Any
from django import forms
from django.core.exceptions import ValidationError
from collections import defaultdict

from recipes.models import Recipe
from utils.django_forms import add_attr
from utils.strings import is_positive_number


class AuthorRecipeValidator:
    def __init__(self, data, errors=None, ErrorClass=None):
        self.errors = defaultdict(list) if errors is None else errors
        self.ErrorClass = ValidationError if ErrorClass is None else ErrorClass
        self.data = data
        self.clean()
    
    def clean(self, *args, **kwargs):
        self.clean_title()
        self.clean_servings()
        self.clean_preparation_time()

        cleaned_data = self.data
        
        title = cleaned_data.get('title')
        description = cleaned_data.get('description')

        if description == title:
            self.errors['description'].append("The description can't be equal to the title")
            self.errors['title'].append("The title can't be equal to the description")

        if self.errors:
            raise self.ErrorClass(self.errors)

    
    def clean_title(self):
        title = self.data.get('title')

        if len(title) < 5:
            self.errors['title'].append('Title must have at least 5 chars.')

        return title
    
    def clean_preparation_time(self):
        field_name = 'preparation_time'
        field_value = self.data.get(field_name)

        if not is_positive_number(field_value):
            self.errors[field_name].append("Must be a positive number")

        return field_value
    
    def clean_servings(self):
        field_name = 'servings'
        field_value = self.data.get(field_name)

        if not is_positive_number(field_value):
            self.errors[field_name].append("Must be a positive number")

        return field_value
    
    