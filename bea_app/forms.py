from django import forms
from django.forms import Textarea
from .models import *
from .choices import *

class UserForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50,required=True)
    last_name = forms.CharField(max_length=50,required=True)
    email = forms.CharField(max_length=50,required=True)
    zip_code = forms.CharField(label="Zip Code",max_length=50,required=True)
    organization = forms.ModelChoiceField(queryset=Organization.objects.all().order_by('name'))
    password = forms.CharField(widget=forms.PasswordInput(),required=True)
    confirm_password=forms.CharField(label="Confirm Password",widget=forms.PasswordInput(),required=True)
    class Meta:
        model = User
        fields = ('email','first_name','last_name','zip_code','password')

    def __init__(self, *args, **kwargs):
        organization_id = kwargs.pop('organization_id', None)
        if organization_id is not None:
            if Organization.objects.filter(pk=organization_id).exists():
                kwargs.update(initial={
                    'organization': organization_id
                })
        super(UserForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if User.objects.filter(username=email).exists():
            # check if email is being used
            msg = "Email is already being used."
            self.add_error('email', msg)
            return cleaned_data

        if password != confirm_password:
            # check if password and confirm password are the same
            msg = "Passwords don't match."
            self.add_error('password', msg)
            return cleaned_data

        return cleaned_data
class LocationForm(forms.ModelForm):
    address = forms.CharField(max_length=50,required=True)
    city = forms.CharField(max_length=50,required=True)
    state = forms.ChoiceField(choices=STATE_CHOICES)
    zip_code = forms.IntegerField()
    class Meta:
        model = Location
        fields = ('address','city','state','zip_code')

class ActForm(forms.ModelForm):
    name = forms.CharField(max_length=50,required=True)
    details = forms.CharField(max_length=200,required=True,widget=forms.Textarea)
    public = forms.BooleanField(required=False)
    class Meta:
        model = Act
        fields = ('name','details')
        widgets = {
            'details': Textarea(attrs={'cols': 20, 'rows': 5}),
        }
