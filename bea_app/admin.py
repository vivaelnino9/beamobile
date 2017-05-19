from django.contrib import admin
from django import forms
from .models import *

class UserAdminForm(forms.ModelForm):
    model = User

class UserAdmin(admin.ModelAdmin):
    list_display = ('username','first_name','last_name','zip_code','points')
    search_fields = ['username',]
    list_per_page = 20
    form = UserAdminForm

admin.site.register(User,UserAdmin)
