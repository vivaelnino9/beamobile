from django import forms
from .models import *

class UserForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50,required=True)
    last_name = forms.CharField(max_length=50,required=True)
    email = forms.CharField(max_length=50,required=True)
    zip_code = forms.CharField(label="Zip Code",max_length=50,required=True)
    password = forms.CharField(widget=forms.PasswordInput(),required=True)
    confirm_password=forms.CharField(label="Confirm Password",widget=forms.PasswordInput(),required=True)
    class Meta:
        model = User
        fields = ('email','first_name','last_name','zip_code','password')

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
