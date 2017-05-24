from django.contrib import admin
from django import forms
from .models import *

class UserAdminForm(forms.ModelForm):
    model = User

class UserAdmin(admin.ModelAdmin):
    list_display = ('username','first_name','last_name','zip_code','points')
    search_fields = ['username',]
    list_filter = ['zip_code','points',]
    list_per_page = 20
    form = UserAdminForm

admin.site.register(User,UserAdmin)

class ChallengeAdminForm(forms.ModelForm):
    model = Challenge

class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('name','date_start','date_end','points',)
    search_fields = ['name',]
    list_filter = ['date_start','date_end','points',]
    list_per_page = 20
    form = ChallengeAdminForm

admin.site.register(Challenge,ChallengeAdmin)
