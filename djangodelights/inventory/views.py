from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from .models import Ingredient, MenuItem, Purchase
from django.http import Http404
from django.shortcuts import render, redirect
from .forms import IngredientCreateForm, IngredientUpdateForm, MenuItemCreateForm, MenuItemUpdateForm, PurchaseCreateForm
from django.urls import reverse_lazy
import pint
import datetime
# Create your views here.

def signIn(request):
    username = request.POST["username"]
    password = request.POST["password"]

    user = authenticate(request,username,password)

    if user is not None:
        login(request,user)
    else:
        return Http404("user does not exist")
    return render(request,"inventory/home.html",user)

class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("login")

@login_required
def signOut(request):
    logout(request)
    return redirect("login")


class IngredientListView(LoginRequiredMixin, ListView):
    model = Ingredient
    template_name = "inventory/ingredients.html"

class IngredientCreateView(LoginRequiredMixin, CreateView):
    model = Ingredient
    form_class = IngredientCreateForm
    template_name = "inventory/addingredient.html"
    success_url = reverse_lazy("ingredients")

    def post(self,request):
        ureg = pint.UnitRegistry()
        unit_of_measure = request.POST["unit_of_measurement"]
        quantity = request.POST["available_quantity"]
        mv = quantity * ureg[unit_of_measure]
        new_ingredient = Ingredient(request.POST["name"], mv, request.POST["price_per_unit"])
        new_ingredient.save()

class IngredientUpdateView(LoginRequiredMixin, UpdateView):
    model = Ingredient
    form_class = IngredientUpdateForm
    template_name = "inventory/updateingredient.html"
    success_url = reverse_lazy("Ingredients")

    def post(self, request):
        ureg = pint.UnitRegistry()
        unit_of_measure = request.POST["unit_of_measurement"]
        quantity = request.POST["available_quantity"]
        mv = quantity * ureg[unit_of_measure]
        ing = Ingredient.objects.get(pk=self.kwargs["pk"])
        ing.name = request.POST['name']
        ing.available_quantity = mv
        ing.price_per_unit = request.POST['price_per_unit']
        ing.save()
    

class IngredientDeleteView(LoginRequiredMixin, DeleteView):
    model = Ingredient
    success_url = reverse_lazy("ingredients")

class MenuItemListView(LoginRequiredMixin, ListView):
    model = MenuItem
    template_name = "inventory/Menu.html"

class MenuItemCreateView(LoginRequiredMixin, CreateView):
    model = MenuItem
    form_class = MenuItemCreateForm
    template_name = "inventory/addmenuitem.html"
    success_url = reverse_lazy("menu")

class MenuItemUpdateView(LoginRequiredMixin, UpdateView):
    model = MenuItem
    form_class = MenuItemUpdateForm
    template_name = "inventory/updatemenuitem.html"
    success_url = reverse_lazy("menu")

    def post(self, request):
        mi = MenuItem.objects.get(pk=self.kwargs["pk"])
        mi.name = request.POST["name"]
        mi.price = request.POST["price"]
        mi.recipeRequirements = request.POST["recipeRequirements"]
        mi.save()

class MenuItemDeleteView(LoginRequiredMixin, DeleteView):
    model = MenuItem
    success_url = reverse_lazy("menu")

class PurchaseListView(LoginRequiredMixin, ListView):
    model = Purchase
    success_url = reverse_lazy("inventory/purchases.html")

class PurchaseCreateView(LoginRequiredMixin, CreateView):
    model = Purchase
    form_class = PurchaseCreateForm
    template_name = "inventory/createpurchase.html"
    success_url = reverse_lazy("purchases")

    def post(self,request):
        ingredients = []
        prices = []
        for menu_item in list(request.POST.menu_items.all()):
            ingredients.append(MenuItem.objects.get(name=menu_item).recipe_requirements)
            prices.append(MenuItem.objects.get(name=menu_item).price)
        total_ingredients = [ingredient for row in ingredients for ingredient in row]
        total_prices = sum(prices)
        for ing in total_ingredients:
            ureg = pint.UnitRegistry()
            unit_of_measure = ing["unit_of_measurement"]
            quantity = ing["quantity"]
            mv = quantity * ureg[unit_of_measure]
            x = Ingredient.objects.get(ingredient=ing.ingredient)
            if x.available_quantity >= mv:
                x.available_quantity -= mv
            else:
                return "not enough ingredients for purchase!"
        new_purchase = Purchase(request.POST["menu_items"], datetime.now, total_prices)
        new_purchase.save()

class PurchaseDeleteView(LoginRequiredMixin, DeleteView):
    model = Purchase
    success_url = reverse_lazy("purchases")

    def post(self, request):
        ingredients = []
        for menu_item in list(request.POST.menu_items.all()):
            ingredients.append(MenuItem.objects.get(name=menu_item).recipe_requirements)
        total_ingredients = [ingredient for row in ingredients for ingredient in row]
        for ing in total_ingredients:
            ureg = pint.UnitRegistry()
            unit_of_measure = ing["unit_of_measurement"]
            quantity = ing["quantity"]
            mv = quantity * ureg[unit_of_measure]
            x = Ingredient.objects.get(ingredient=ing.ingredient)
            x.available_quantity += mv
        purchase = Purchase.objects.get(pk=self.kwargs['pk'])
        purchase.delete()