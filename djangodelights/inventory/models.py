from django.db import models
from django_jsonform.models.fields import JSONField
from datetime import datetime
from django_measurement.models import MeasurementField
from measurement.measures import Volume
from .choices_list import list_of_choices

# Create your models here.

class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    available_quantity = MeasurementField(measurement=Volume)
    price_per_unit = models.FloatField()

    def __str__(self):
        return self.name

class MenuItem(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField()
    recipeRequirements = JSONField(schema={
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "ingredient": {"type": "string"},
                "quantity": {"type": "integer"},
                "unit_of_measurement": {"type": "string",
                                        "choices": list_of_choices }
            }
        }
    })

    def __str__(self):
        return self.name

class Purchase(models.Model):
    menu_items = models.ManyToManyField(MenuItem)
    time_of_purchase = models.DateTimeField(default=datetime.now)
    total = models.FloatField()

    def __str__(self):
        mi = []
        for i in list(self.menu_items.all()):
            mi.append(i)
        return str(mi)

    class Meta:
        ordering = ['time_of_purchase']
