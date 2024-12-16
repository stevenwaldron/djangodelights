from django import forms 
from .models import Ingredient, MenuItem, Purchase
from django_jsonform.forms.fields import JSONFormField
from .choices_list import list_of_choices

class IngredientCreateForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ["ingredient_fields"]

    ingredient_fields = JSONFormField(schema={
                "name": {"type": "string"},
                "price_per_unit": {"type": "float"},
                "available_quantity": {"type": "integer"},
                "unit_of_measurement": {"type": "string",
                                        "choices": list_of_choices }
            })

class IngredientUpdateForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ["ingredient_fields"]

        ingredient_fields = JSONFormField(schema={
                "name": {"type": "string"},
                "price_per_unit": {"type": "float"},
                "available_quantity": {"type": "integer"},
                "unit_of_measurement": {"type": "string",
                                        "choices": list_of_choices }
            })

class MenuItemCreateForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ["name", "price", "recipeRequirements"]

    recipeRequirements = JSONFormField(schema={
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

class MenuItemUpdateForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ["name", "price", "recipeRequirements"]

    recipeRequirements = JSONFormField(schema={
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

class PurchaseCreateForm(forms.ModelForm):
    menu_items = forms.ModelMultipleChoiceField(queryset=MenuItem.objects.all(), Widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Purchase
        fields = ["menu_items"]

