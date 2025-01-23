import pint
from pint.errors import UndefinedUnitError
from django.core.exceptions import ValidationError
from .models import MenuItem, Ingredient
import json
from django.contrib.auth.models import User


def validate_ingredient_unit_of_measure(value):
    ureg = pint.UnitRegistry()
    try:
        single_unit = ureg[value]
    except UndefinedUnitError as e:
        raise ValidationError("not a valid unit of measure.")
    except Exception as error:
        raise ValidationError(f"validator: '{value}' is not valid. {error} ")
    
def validate_unit_of_measure(value):
    print(value,type(value))
    for object in value:
        print(object['unit_of_measurement'])
        try:
            ureg = pint.UnitRegistry()
            single_unit = ureg[object['unit_of_measurement']]
        except UndefinedUnitError as e:
            raise ValidationError(f"'{object['unit_of_measurement']}' is not a valid unit of measure.")
        except Exception as error:
            print(value,type(value))
            raise ValidationError(f"validator: '{value}' is not valid. {error} ")
        
def validate_purchase_create(value):
    print(value,type(value))
    ingredients = []
    prices = []
    l = []  
    menuitems = value
    for item in menuitems:
        l.append(item)
        for menu_item in l:
            data = MenuItem.objects.get(pk=menu_item).recipeRequirements
            if isinstance(data, str):
                print('this is a string')
                parsed_data = json.loads(data)
                print(parsed_data, type(parsed_data))
                ingredients.append(parsed_data)
                prices.append(MenuItem.objects.get(pk=menu_item).price)
            else:
                ingredients.append(data)
                prices.append(MenuItem.objects.get(pk=menu_item).price)
        total_ingredients = [ingredient for row in ingredients for ingredient in row]
        for ing in total_ingredients:
            ureg = pint.UnitRegistry()
            unit_of_measure = ing["unit_of_measurement"]
            quantity = ing["quantity"]
            mv = quantity * ureg[unit_of_measure]
            try:
                tracker = []
                x = Ingredient.objects.get(name=ing['ingredient'])
                if (x.available_quantity * ureg[x.unit_of_measurement]) >= mv:
                    tracker.append({'ingredient':x, 'quan':mv})
                    print('enough on hand')
                else:
                    if len(tracker) != 0:
                        for i in tracker:
                            i['ingredient'].available_quantity += quantity
                    raise ValidationError("not enough ingredients on hand for purchase!") 
            except Ingredient.DoesNotExist:
                raise ValidationError(f'sorry! missing ingredients neccessary for this purchase {ing}')
            
    


