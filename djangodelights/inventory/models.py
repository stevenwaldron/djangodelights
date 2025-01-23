from django.db import models
from django_jsonform.models.fields import JSONField
from datetime import datetime
from django_measurement.models import MeasurementField
from measurement.measures import Volume
from .choices_list import list_of_choices
from djmoney.models.fields import MoneyField


# Create your models here.

class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    available_quantity = models.FloatField()
    price_per_unit = MoneyField(max_digits=14,decimal_places=2 ,default_currency='USD', default=0)
    unit_of_measurement = models.CharField(max_length=100, default='')

    def __str__(self):
        return self.name

class MenuItem(models.Model):
    name = models.CharField(max_length=200)
    price = MoneyField(max_digits=14,decimal_places=2 ,default_currency='USD', default=0)
    recipeRequirements = JSONField(schema={
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "ingredient": {"type": "string"},
                "quantity": {"type": "number"},
                "unit_of_measurement": {"type": "string"}
            }
        }
    })

    def __str__(self):
        return self.name

class Purchase(models.Model):
    menu_items = models.ManyToManyField(MenuItem)
    time_of_purchase = models.DateTimeField(default=datetime.now)
    total = MoneyField(max_digits=14,decimal_places=2 ,default_currency='USD', default=0)

    class Meta:
        ordering = ['time_of_purchase']
