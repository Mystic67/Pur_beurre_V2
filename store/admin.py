from django.contrib import admin
from .models import Categories, Products, Nutriments_for_100g, User_Favorites_Substitutes

admin.site.register(Categories)
admin.site.register(Products)
admin.site.register(Nutriments_for_100g)
admin.site.register(User_Favorites_Substitutes)
