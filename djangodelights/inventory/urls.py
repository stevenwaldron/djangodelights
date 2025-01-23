from django.urls import path
from . import views 
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("home/", views.HomeView, name="home"),
    path("signin/", views.MyLoginView.as_view(),name="signin"),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("logout/", views.signOut, name="logout"),
    path("contact/", views.ContactView, name="contact"),
    path("ingredients/", views.IngredientListView.as_view(), name="ingredients"),
    path("ingredient/add/", views.IngredientCreateView.as_view(), name="/addingredient/" ),
    path("ingredient/<int:pk>/update/", views.IngredientUpdateView.as_view(), name='/updateingredient/'),
    path("ingredient/<int:pk>/delete/", views.IngredientDeleteView.as_view(), name='/deleteingredient/'),
    path("menu/", views.MenuItemListView.as_view(), name="menu" ),
    path("menu/additem/", views.MenuItemCreateView.as_view(), name="/addmenuitem/"),
    path("menu/<int:pk>/update", views.MenuItemUpdateView.as_view(), name="/updatemenuitem/"),
    path("menu/<int:pk>/delete/", views.MenuItemDeleteView.as_view(), name= "/deletemenuitem/"),
    path("purchases/", views.PurchaseListView.as_view(), name='purchases'),
    path("purchase/<int:pk>/delete/", views.PurchaseDeleteView.as_view(), name="/deletepurchase/"),
    path("purchase/<int:pk>/deleteandrestore/", views.PurchaseDeleteAndRestoreView.as_view(), name="/deleteandrestorepurchase/"),
    path("purchase/add/", views.PurchaseCreateView.as_view(), name="/addpurchase/"),
    path("password-reset/", auth_views.PasswordResetView.as_view(template_name='passwordReset/password_reset.html'), name="password_reset"),
    path("password-reset/done/", auth_views.PasswordResetDoneView.as_view(template_name='passwordReset/password_reset_done.html'), name="password_reset_done"),
    path("password-reset-confirm/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name='passwordReset/password_reset_confirm.html'), name="password_reset_confirm"),
    path("password-reset-complete/", auth_views.PasswordResetCompleteView.as_view(template_name='passwordReset/password_reset_complete.html'), name="password_reset_complete"),


]