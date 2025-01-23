from django import forms 
from .models import Ingredient, MenuItem, Purchase
from django_jsonform.forms.fields import JSONFormField
from .choices_list import list_of_choices
from .validators import validate_unit_of_measure, validate_ingredient_unit_of_measure, validate_purchase_create
from django.core import validators
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm

class IngredientCreateForm(forms.ModelForm):
    unit_of_measurement = forms.CharField(validators=[validate_ingredient_unit_of_measure])

    class Meta:
        model = Ingredient
        fields = ("name","price_per_unit","available_quantity","unit_of_measurement")

class IngredientUpdateForm(forms.ModelForm):
    unit_of_measurement = forms.CharField(validators=[validate_ingredient_unit_of_measure])

    class Meta:
        model = Ingredient
        fields = "__all__"


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
                "quantity": {"type": "number"},
                "unit_of_measurement": {"type": "string"}
               
            }, "required": ["ingredient","quantity","unit_of_measurement"]
        }
    }, validators=[validate_unit_of_measure])
        

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
                "quantity": {"type": "number"},
                "unit_of_measurement": {"type": "string"}
            }, "required": ["ingredient","quantity","unit_of_measurement"]
        }
    }, validators=[validate_unit_of_measure])

class PurchaseCreateForm(forms.ModelForm):
    menu_items = forms.ModelMultipleChoiceField(queryset=MenuItem.objects.all(), validators=[validate_purchase_create])

    class Meta:
        model = Purchase
        fields = ["menu_items"]

class CustomSigninForm(AuthenticationForm):
    username = forms.CharField()
    password = forms.CharField()

    def clean(self):
        cleaned_data = super().clean()

        user_name = cleaned_data.get('username')
        passWord = cleaned_data.get('password')

        try:
            user = User.objects.get(username=user_name)
        except User.DoesNotExist:
            raise ValidationError('Please enter a correct username and password. Note that both fields may be case-sensitive.')
        if user.check_password(passWord) == False:
            raise ValidationError('Please enter a correct username and password. Note that both fields may be case-sensitive.')
        
        return cleaned_data
    

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(label=("Email"), required=True)

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email',)