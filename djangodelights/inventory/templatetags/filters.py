from django import template
from inventory.models import Purchase
import json

register = template.Library()

@register.filter
def list_items(value):
    print(value)
    string = ""
    print(list(Purchase.objects.get(pk=value).menu_items.all()))
    for item in list(Purchase.objects.get(pk=value).menu_items.all()):
        string += ((str(item)) + ", ")
    new_string = string[:-2]
    return new_string

@register.filter
def list_recipe_requirements(value):
    print("value",value, type(value))
    parsed_value = json.loads(value)
    string = ''
    for object in parsed_value:
        print('parsed object', object, object['quantity'])
        string += f"{object['quantity']} {object['unit_of_measurement']} of {object['ingredient']},\n"
    new_string = string[:-2]
    return new_string

@register.filter
def remove_dot(value):
    print('value', value)