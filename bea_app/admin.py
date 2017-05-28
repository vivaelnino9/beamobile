from django.contrib import admin
from django import forms
from .models import *
from .choices import *

class UserAdminForm(forms.ModelForm):
    model = User

class UserAdmin(admin.ModelAdmin):
    list_display = ('username','first_name','last_name','zip_code','get_points','organization')
    search_fields = ['username',]
    list_filter = ['zip_code','organization']
    list_per_page = 20
    form = UserAdminForm

    def get_points(self,obj):
        return obj.get_points()
    get_points.short_description = 'Points'
    
admin.site.register(User,UserAdmin)

class ChallengeStatusAdminForm(forms.ModelForm):
    model = Challenge_Status

class ChallengeStatusAdmin(admin.ModelAdmin):
    list_display = ('user','challenge','get_status','location','feeling','date_completed')
    search_fields = ['user','challenge']
    list_filter = ['user','challenge','date_completed']
    list_per_page = 20
    form = ChallengeStatusAdminForm

    def get_status(self,obj):
        return dict(STATUS_CHOICES).get(int(obj.status))
    get_status.short_description = 'Status'

admin.site.register(Challenge_Status,ChallengeStatusAdmin)

class OrganizationAdminForm(forms.ModelForm):
    model = Organization

class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name',]
    list_filter = []
    list_per_page = 20
    form = OrganizationAdminForm

admin.site.register(Organization,OrganizationAdmin)

class LocationAdminForm(forms.ModelForm):
    model = Location

class LocationAdmin(admin.ModelAdmin):
    list_display = ('address','city','state','zip_code')
    search_fields = ['city','state',]
    list_filter = ['city','state',]
    list_per_page = 20
    form = LocationAdminForm

admin.site.register(Location,LocationAdmin)

class ChallengeAdminForm(forms.ModelForm):
    model = Challenge

class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('name','date_start','date_end','points',)
    search_fields = ['name',]
    list_filter = ['date_start','date_end','points',]
    list_per_page = 20
    form = ChallengeAdminForm

admin.site.register(Challenge,ChallengeAdmin)

class ActAdminForm(forms.ModelForm):
    model = Act

class ActAdmin(admin.ModelAdmin):
    list_display = ('user','name','public',)
    search_fields = ['user','name',]
    list_filter = ['public',]
    list_per_page = 20
    form = ActAdminForm

admin.site.register(Act,ActAdmin)
