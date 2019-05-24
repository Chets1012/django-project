import datetime
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.forms.widgets import SelectDateWidget
# from blog.model import post
from .models import User
from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import AuthenticationForm

class UserRegistrationForm(UserCreationForm):
    birth_date = forms.DateField(
      widget=SelectDateWidget(years=range(1940, 2010))
      )

    class Meta:
        model = User
        fields = ["full_name",
                  "gender",
                  "birth_date",
                  "email",
                  "contact_no",
                  "Address",
                  "nationality",
                  "occupation",
                  "picture",
                  "password1",
                  "password2",
                  "degree"
                  ]

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['full_name']
        user.birth_date = self.cleaned_data['birth_date']
        if commit:
            user.save()
        return user


class UserLoginForm(forms.Form):
    email = forms.EmailField(label="Account Number")
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if email and password:
            user_obj = User.objects.filter(email=email).first()
            if user_obj:
                user = authenticate(email=user_obj.email, password=password)
                if not user:
                    raise forms.ValidationError("Account Does Not Exist.")
                if not user.check_password(password):
                    raise forms.ValidationError("Password Does not Match.")
                if not user.is_active:
                    raise forms.ValidationError("Account is not Active.")
            else:
                raise forms.ValidationError("Account Does Not Exist.")

        return super(UserLoginForm, self).clean(*args, **kwargs)


username_regex_field = forms.RegexField(
    label='Username',
    max_length=30,
    regex=r'^[a-z0-9-_]+$',
    error_messages={
        'required': 'Please enter your name',
        'invalid': 'Lowercase alphanumeric characters and underscores and dashes only (a-z, 0-9, _, -)'
    },
)

password_char_field = forms.CharField(
    label='Password',
    max_length=30,
    widget=forms.PasswordInput,
)

confirm_password_char_field = forms.CharField(
    label='Confirm Password',
    max_length=30,
    widget=forms.PasswordInput,
)

class ProfileForm(forms.Form):
    username = username_regex_field
    full_name = forms.RegexField(
        label='First Name',
        max_length=30,
        regex=r'^[a-zA-Z-_]+$',
        error_messages={'invalid': 'Alphabetical, underscores, and dashes only (a-z, A-Z, _, -)'},
        required=False,
    )
    last_name = forms.RegexField(
        label='First Name',
        max_length=30,
        regex=r'^[a-zA-Z-_]+$',
        error_messages={'invalid': 'Alphabetical, underscores, and dashes only (a-z, A-Z, _, -)'},
        required=False,
    )
    email = forms.EmailField(
        label='First Name',
        max_length=50,
        required=False,
    )
    password = password_char_field
    confirm_password = confirm_password_char_field

    def clean(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password and password != confirm_password:
            raise forms.ValidationError("Passwords don't match")

        return self.cleaned_data

class UserForm(forms.ModelForm):

    # The solution originally retrieved from
    #
    # https://stackoverflow.com/questions/33452278/how-to-add-bootstrap-class-to-django-createview-form-fields-in-the-template
    #
    # Thanks to César

    def __init__(self, *args, **kwargs):

        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['full_name'].widget.attrs = {
            'class': 'form-control input-lg'
        }
        self.fields['gender'].widget.attrs = {
            'class': 'form-control'
        }
        self.fields['birth_date'].widget.attrs = {
            'class': 'form-control'
        }
        self.fields['email'].widget.attrs = {
            'class': 'form-control'
        }
        self.fields['contact_no'].widget.attrs = {
            'class': 'form-control'
        }
        self.fields['Address'].widget.attrs = {
            'class': 'form-control'
        }
        self.fields['nationality'].widget.attrs = {
            'class': 'form-control'
        }
        self.fields['occupation'].widget.attrs = {
            'class': 'form-control'
        }
        self.fields['picture'].widget.attrs = {
            'class': 'form-control'
        }
        self.fields['degree'].widget.attrs = {
            'class': 'form-control'
        }


    class Meta:
        model = User
        fields = ('full_name', 'gender', 'birth_date','email','contact_no','Address','nationality','occupation','picture','degree')