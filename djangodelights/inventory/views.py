from django.shortcuts import render, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView 
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from .models import Ingredient, MenuItem, Purchase
from django.http import Http404
from django.shortcuts import render, redirect
from .forms import IngredientCreateForm, IngredientUpdateForm, MenuItemCreateForm, MenuItemUpdateForm, PurchaseCreateForm, CustomUserCreationForm
from django.urls import reverse_lazy
import pint
from pint.errors import UndefinedUnitError
import datetime
from django.http import QueryDict
import json
from .forms import CustomSigninForm
from django.contrib.auth.models import User
# Create your views here.

class MyLoginView(LoginView):
    template_name = 'registration/signin.html'
    success_url = 'inventory/home.html'


    def post(self,request, *args, **kwargs):
        if 'Signup' in request.POST:
            return redirect("signup")
        else:
            super().post(request, *args, **kwargs)
        userName = request.POST["username"]
        passWord = request.POST["password"]
        form = CustomSigninForm(request,data=request.POST)
        if form.is_valid():
            user = authenticate(username=userName,password=passWord)
            userobject = User.objects.get(username=user)
            if user is not None:
                login(request,user)
            else:
                return Http404("user does not exist")
            return redirect("home")
        else:
            return render(request, 'registration/signin.html', {'form': form})

    

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("signin")

@login_required
def signOut(request):
    logout(request)
    print("logged out")
    return redirect("signin")

@login_required
def HomeView(request):
    return render(request, "inventory/home.html")

@login_required
def ContactView(request):
    return render(request, "inventory/contact.html")


class IngredientListView(LoginRequiredMixin, ListView):
    model = Ingredient
    template_name = "inventory/ingredients.html"


class IngredientCreateView(LoginRequiredMixin, CreateView):
    model = Ingredient
    form_class = IngredientCreateForm
    template_name = "inventory/addingredient.html"
    success_url = reverse_lazy("ingredients")

    @method_decorator(csrf_protect)
    def post(self,request, *args, **kwargs):
        if 'cancel' in request.POST:
            return redirect("ingredients")
        print('post method invoked')
        print(request.POST)
        form = IngredientCreateForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            print("form is valid")
            unit_of_measure = request.POST["unit_of_measurement"]
            quantity = request.POST["available_quantity"]
            new_ingredient = Ingredient(name=request.POST["name"], available_quantity=quantity, unit_of_measurement=unit_of_measure, price_per_unit=request.POST["price_per_unit_0"], price_per_unit_currency=request.POST['price_per_unit_1'])
            new_ingredient.save()
            print('end of post method')
            return redirect('ingredients')
        else:
            return render(request, 'inventory/addingredient.html', {'form': form})
        

       

class IngredientUpdateView(LoginRequiredMixin, UpdateView):
    model = Ingredient
    form_class = IngredientUpdateForm
    template_name = "inventory/updateingredient.html"
    success_url = reverse_lazy("ingredients")

    def post(self, request, *args, **kwargs):
        if 'cancel' in request.POST:
            return redirect('ingredients')
        else:
            super().post(request, *args, **kwargs)
        print('post method invoked')
        ureg = pint.UnitRegistry()
        unit_of_measure = request.POST["unit_of_measurement"]
        quantity = request.POST["available_quantity"] 
        form = IngredientUpdateForm(request.POST)
        if form.is_valid():
            ing = Ingredient.objects.get(pk=self.kwargs["pk"])
            ing.name = request.POST['name']
            ing.available_quantity = quantity
            ing.unit_of_measurement = unit_of_measure
            ing.price_per_unit = request.POST['price_per_unit_0']
            ing.save()
            return redirect('ingredients')
        else:
            return render(request, 'inventory/updateingredient.html', {'form': form})
        
    

class IngredientDeleteView(LoginRequiredMixin, DeleteView):
    model = Ingredient
    template_name = 'inventory/deleteingredient.html'
    success_url = reverse_lazy("ingredients")

    def post(self, request, *args, **kwargs):
        if 'cancel' in request.POST:
            return redirect('ingredients')
        else:
            return super().post(request, *args, **kwargs)

class MenuItemListView(LoginRequiredMixin, ListView):
    model = MenuItem
    template_name = "inventory/Menu.html"

class MenuItemCreateView(LoginRequiredMixin, CreateView):
    model = MenuItem
    form_class = MenuItemCreateForm
    template_name = "inventory/addmenuitem.html"
    success_url = reverse_lazy("menu")

    @method_decorator(csrf_protect)
    def post(self,request, *args, **kwargs):
        if 'cancel' in request.POST:
            return redirect('menu')
        print("MenuItemCreateView post method invoked")
        print(request.POST, type(request.POST["recipeRequirements"]))
        regdict = dict(request.POST.copy())
        print(regdict)
        # regdict["recipeRequirements"] = f"{regdict['recipeRequirements']}"
        print(regdict, type(regdict['recipeRequirements']))
        price = request.POST["price_0"]
        currency = request.POST["price_1"]
        print(price)
        name = request.POST["name"]
        print(name)
        token = request.POST['csrfmiddlewaretoken']
        recipierequirements = request.POST["recipeRequirements"]
        ing = request.POST['rjf§0§ingredient']
        quan = request.POST['rjf§0§quantity']
        rr = request.POST['rjf§0§unit_of_measurement']
        print(recipierequirements, type(recipierequirements))
        form = MenuItemCreateForm(request.POST)
        # form = MenuItemCreateForm({'csrfmiddlewaretoken':token}, {'name':name}, {'price_0': price}, {'price_1': currency}, {'rjf§0§ingredient': ing}, {'rjf§0§quantity': quan}, {'rjf§0§unit_of_measurement': rr}, {'recipeRequirements': recipierequirements})
        # print(form)
        print(form.is_valid())
        if form.is_valid():
            print(form.cleaned_data)
            menuitem = MenuItem()
            menuitem.name = name
            menuitem.price = price 
            menuitem.recipeRequirements = recipierequirements
            menuitem.save()
            return redirect("menu")
        else:
            print("form is NOT valid.")
            return render(request, 'inventory/addmenuitem.html', {'form': form})


class MenuItemUpdateView(LoginRequiredMixin, UpdateView):
    model = MenuItem
    form_class = MenuItemUpdateForm
    template_name = "inventory/updatemenuitem.html"
    success_url = reverse_lazy("menu")

    def post(self, request, *args, **kwargs):
        if 'cancel' in request.POST:
            return redirect('menu')
        mi = MenuItem.objects.get(pk=self.kwargs["pk"])
        form = MenuItemUpdateForm(request.POST)
        if form.is_valid():      
            mi.name = request.POST["name"]
            mi.price = request.POST["price_0"]
            mi.recipeRequirements = request.POST["recipeRequirements"]
            mi.save()
            return redirect("menu")
        else:
            print("form is NOT valid.")
            return render(request, 'inventory/updatemenuitem.html', {'form': form})

class MenuItemDeleteView(LoginRequiredMixin, DeleteView):
    model = MenuItem
    template_name = "inventory/deletemenuitem.html"
    success_url = reverse_lazy("menu")

    def post(self,request, *args, **kwargs):
        if 'cancel' in request.POST:
            return redirect('menu')
        else:
            super().post(request, *args, **kwargs)
            return redirect('menu')

class PurchaseListView(LoginRequiredMixin, ListView):
    model = Purchase
    template_name = "inventory/purchases.html"

class PurchaseCreateView(LoginRequiredMixin, CreateView):
    model = Purchase
    form_class = PurchaseCreateForm
    template_name = "inventory/addpurchase.html"
    success_url = reverse_lazy("purchases")

    @method_decorator(csrf_protect)
    def post(self,request, *args, **kwargs):
        if 'cancel' in request.POST:
            return redirect('purchases')
        ingredients = []
        prices = []
        l = []
        mutable_copy = dict(request.POST.copy())
        menuitems = dict(request.POST.copy())["menu_items"]
        print("menuitems", menuitems, type(menuitems))
        for item in menuitems:
            print(item)
            l.append(item)
        print("l",l)
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
        total_prices = sum(prices)
        print("ingredients", ingredients)
        print("total_ingredients", total_ingredients)
        print("total_prices", total_prices)
        form = PurchaseCreateForm(request.POST)
        if form.is_valid():
            print("form is valid.")
            for ing in total_ingredients:
                print(ing["ingredient"])
                ureg = pint.UnitRegistry()
                unit_of_measure = ing["unit_of_measurement"]
                quantity = ing["quantity"]
                mv = quantity * ureg[unit_of_measure]
                x = Ingredient.objects.get(name=ing['ingredient'])
                remainder = (x.available_quantity * ureg[x.unit_of_measurement]) - mv
                remainder_values = str(remainder).split()
                quan = remainder_values[0]
                unitOfMeasure = remainder_values[1]
                x.available_quantity = float(quan)
                x.unit_of_measurement = unitOfMeasure
                x.save()
            newPurchase = Purchase()
            newPurchase.save()
            latest = Purchase.objects.last()
            for item in menuitems:
                latest.menu_items.add(item)
            latest.total = total_prices
            latest.save()
            return redirect("purchases")
        else:
            print('form invalid')
            print(form.errors)
            return render(request, "inventory/addpurchase.html", {"form": form})
        
class PurchaseDeleteView(LoginRequiredMixin, DeleteView):
    model = Purchase
    template_name = "inventory/deletepurchase.html"
    success_url = reverse_lazy("purchases")

    def post(self, request, *args, **kwargs):
        if 'cancel' in request.POST:
            return redirect('purchases')
        else:
            return super().post(request, *args, **kwargs)

class PurchaseDeleteAndRestoreView(LoginRequiredMixin, DeleteView):
    model = Purchase
    template_name = "inventory/deleteandrestorepurchase.html"
    success_url = reverse_lazy("purchases")

    def post(self, request, *args, **kwargs):
        if 'cancel' in request.POST:
            return redirect('purchases')
        ingredients = []
        print(kwargs)
        purchase = Purchase.objects.get(pk=self.kwargs['pk'])
        mi = list(purchase.menu_items.all())
        print(mi, type(mi))
        for menu_item in mi:
            data = MenuItem.objects.get(name=menu_item).recipeRequirements
            if isinstance(data, str):
                print('this is a string')
                parsed_data = json.loads(data)
                print(parsed_data, type(parsed_data))
                ingredients.append(parsed_data)
            else:
                ingredients.append(data)
        print('ingredients', ingredients)
        total_ingredients = [ingredient for row in ingredients for ingredient in row]
        print('total ingredients', total_ingredients)
        for ing in total_ingredients:
            try:
                test = Ingredient.objects.get(name=ing['ingredient'])
            except Ingredient.DoesNotExist:
                continue
            print('ing',ing)
            print(list(Ingredient.objects.all()))
            ureg = pint.UnitRegistry()
            unit_of_measure = ing["unit_of_measurement"]
            quantity = ing["quantity"]
            mv = quantity * ureg[unit_of_measure]
            x = Ingredient.objects.get(name=ing['ingredient'])
            new_value = (x.available_quantity * ureg[x.unit_of_measurement]) + mv
            new_values = str(new_value).split()
            quan = new_values[0]
            unitOfMeasure = new_values[1]
            x.available_quantity = float(quan)
            x.unit_of_measurement = unitOfMeasure
            x.save()
        purchase = Purchase.objects.get(pk=self.kwargs['pk'])
        purchase.delete()
        return redirect("purchases")