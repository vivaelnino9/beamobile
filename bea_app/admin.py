from django import forms
from django.contrib import admin
from django.conf.urls import url
from django.contrib.admin import AdminSite
from django.contrib.auth.models import Group
from django.contrib.admin.views.decorators import staff_member_required

from friendship.models import Friend, FriendshipRequest, Follow
from friendship.admin import FriendAdmin
from simple_email_confirmation.models import EmailAddress

from .models import *
from .choices import *

class MyAdminSite(AdminSite):
    site_header = 'Be A Administration'
    site_url = None

admin_site = MyAdminSite(name='admin')


class FriendAdminForm(forms.ModelForm):
    model = Friend

class FriendAdmin(admin.ModelAdmin):
    list_display = ('to_user','from_user','created')
    search_fields = ['to_user','from_user']
    list_filter = ['created']
    list_per_page = 20
    form = FriendAdminForm

    def get_points(self,obj):
        return obj.get_points()
    get_points.short_description = 'Points'

    def has_add_permission(self, request):
        return request.user.groups.filter(name='admin').exists()

    def has_change_permission(self, request, obj=None):
        return request.user.groups.filter(name='admin').exists()

    def has_delete_permission(self, request, obj=None):
        return request.user.groups.filter(name='admin').exists()

admin_site.register(Friend,FriendAdmin)

class FriendshipRequestAdminForm(forms.ModelForm):
    model = FriendshipRequest

class FriendshipRequestAdmin(admin.ModelAdmin):
    list_display = ('to_user','from_user','created')
    search_fields = ['to_user','from_user']
    list_filter = ['created']
    list_per_page = 20
    form = FriendshipRequestAdminForm

    def get_points(self,obj):
        return obj.get_points()
    get_points.short_description = 'Points'

    def has_add_permission(self, request):
        return request.user.groups.filter(name='admin').exists()

    def has_change_permission(self, request, obj=None):
        return request.user.groups.filter(name='admin').exists()

    def has_delete_permission(self, request, obj=None):
        return request.user.groups.filter(name='admin').exists()

admin_site.register(FriendshipRequest,FriendshipRequestAdmin)

class EmailAddressAdminForm(forms.ModelForm):
    model = EmailAddress

class EmailAddressAdmin(admin.ModelAdmin):
    list_display = ('user','email','key','set_at','confirmed_at')
    search_fields = ['user','email']
    list_filter = ['set_at','confirmed_at']
    list_per_page = 20
    form = EmailAddressAdminForm


    def has_add_permission(self, request):
        return request.user.groups.filter(name='admin').exists()

    def has_change_permission(self, request, obj=None):
        return request.user.groups.filter(name='admin').exists()

    def has_delete_permission(self, request, obj=None):
        return request.user.groups.filter(name='admin').exists()

admin_site.register(EmailAddress,EmailAddressAdmin)

class GroupAdminForm(forms.ModelForm):
    model = Group

class GroupAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name']
    list_per_page = 20
    form = GroupAdminForm

    def get_points(self,obj):
        return obj.get_points()
    get_points.short_description = 'Points'

    def has_add_permission(self, request):
        return request.user.groups.filter(name='admin').exists()

    def has_change_permission(self, request, obj=None):
        return request.user.groups.filter(name='admin').exists()

    def has_delete_permission(self, request, obj=None):
        return request.user.groups.filter(name='admin').exists()

admin_site.register(Group,GroupAdmin)


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

    def has_add_permission(self, request):
        return request.user.groups.filter(name='admin').exists()

    def has_change_permission(self, request, obj=None):
        return request.user.groups.filter(name='admin').exists()

    def has_delete_permission(self, request, obj=None):
        return request.user.groups.filter(name='admin').exists()

admin_site.register(User,UserAdmin)

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

    def has_add_permission(self, request):
        return request.user.groups.filter(name='admin').exists()

    def has_change_permission(self, request, obj=None):
        return request.user.groups.filter(name='admin').exists()

    def has_delete_permission(self, request, obj=None):
        return request.user.groups.filter(name='admin').exists()

admin_site.register(Challenge_Status,ChallengeStatusAdmin)

class OrganizationAdminForm(forms.ModelForm):
    model = Organization

class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name',]
    list_filter = []
    list_per_page = 20
    form = OrganizationAdminForm
    def get_queryset(self, request):
        qs = super(OrganizationAdmin, self).get_queryset(request)
        if request.user.groups.filter(name='admin').exists() or request.user.groups.filter(name='bea_admin').exists():
            return qs
        return qs.filter(name=request.user.organization.name)

    def has_add_permission(self, request):
        return request.user.groups.filter(name='admin').exists() or request.user.groups.filter(name='bea_admin').exists()

    def has_delete_permission(self, request, obj=None):
        return request.user.groups.filter(name='admin').exists() or request.user.groups.filter(name='bea_admin').exists()

admin_site.register(Organization,OrganizationAdmin)

class LocationAdminForm(forms.ModelForm):
    model = Location

class LocationAdmin(admin.ModelAdmin):
    list_display = ('address','city','state','zip_code')
    search_fields = ['city','state',]
    list_filter = ['city','state',]
    list_per_page = 20
    form = LocationAdminForm

    def has_add_permission(self, request):
        return request.user.groups.filter(name='admin').exists()

    def has_change_permission(self, request, obj=None):
        return request.user.groups.filter(name='admin').exists()

    def has_delete_permission(self, request, obj=None):
        return request.user.groups.filter(name='admin').exists()

admin_site.register(Location,LocationAdmin)

class ChallengeAdminForm(forms.ModelForm):
    model = Challenge

class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('name','date_start','date_end','points',)
    search_fields = ['name',]
    list_filter = ['date_start','date_end','points',]
    list_per_page = 20
    form = ChallengeAdminForm

    def has_add_permission(self, request):
        return request.user.groups.filter(name='admin').exists() or request.user.groups.filter(name='bea_admin').exists()

    def has_change_permission(self, request):
        return request.user.groups.filter(name='admin').exists() or request.user.groups.filter(name='bea_admin').exists()

    def has_delete_permission(self, request, obj=None):
        return request.user.groups.filter(name='admin').exists() or request.user.groups.filter(name='bea_admin').exists()

admin_site.register(Challenge,ChallengeAdmin)

class ActAdminForm(forms.ModelForm):
    model = Act

class ActAdmin(admin.ModelAdmin):
    list_display = ('user','name','public',)
    search_fields = ['user','name',]
    list_filter = ['public',]
    list_per_page = 20
    form = ActAdminForm

    def has_add_permission(self, request):
        return request.user.groups.filter(name='admin').exists()

    def has_change_permission(self, request, obj=None):
        return request.user.groups.filter(name='admin').exists()

    def has_delete_permission(self, request, obj=None):
        return request.user.groups.filter(name='admin').exists()

admin_site.register(Act,ActAdmin)
