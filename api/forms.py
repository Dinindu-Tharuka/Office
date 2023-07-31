from typing import Any
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Client, Category, Sector, Job
from core.models import User
from django.contrib.auth.forms import UserCreationForm


FORMAT_CHOICES = [
    ('xls', 'xls'),
    ('pdf', 'pdf')
]


class FormFormat(forms.Form):
    format = forms.ChoiceField(
        choices=FORMAT_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))


class ClientDetailForm(forms.ModelForm):
    
    class Meta:
        model = Client
        fields = ['user', 'number', 'nic', 'address', 'date_of_issue', 'birthday', 'gender', 'precent_working_place',
                  'photo', 'is_sri_lanka', 'remark', 'job', 'sector', 'city', 'district', 'province', 'category']

    

class EmailLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
    # email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'autofocus': True}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class':'form-control'}))


class CustomCategory(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

        widgets = {
            'category_title': forms.TextInput(attrs={'class': 'form-control'}),
        }


class CustomSector(forms.ModelForm):
    class Meta:
        model = Sector
        fields = '__all__'

        widgets = {
            'sector_title': forms.TextInput(attrs={'class': 'form-control'}),
        }


class CustomJob(forms.ModelForm):
    class Meta:
        model = Job
        fields = '__all__'

        widgets = {
            'job_title': forms.TextInput(attrs={'class': 'form-control'}),
        }


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'form-control'}), required=True)
    first_name = forms.CharField(
        max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    last_name = forms.CharField(
        max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'email', 'password1', 'password2']

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super(RegistrationForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'



# class UserUpdateForm(forms.ModelForm):
#     email = forms.EmailField(widget=forms.EmailInput(
#         attrs={'class': 'form-control'}), required=True)
#     first_name = forms.CharField(
#         max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
#     last_name = forms.CharField(
#         max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)

#     class Meta:
#         model = User
#         fields = ['username', 'first_name', 'last_name',
#                   'email', 'password1', 'password2']

#     def __init__(self, *args: Any, **kwargs: Any) -> None:
#         super(UserUpdateForm, self).__init__(*args, **kwargs)

#         self.fields['username'].widget.attrs['class'] = 'form-control'
#         self.fields['password1'].widget.attrs['class'] = 'form-control'
#         self.fields['password2'].widget.attrs['class'] = 'form-control'

    
        


