from django.contrib import messages
from django.contrib.auth import (authenticate,
                                 login,
                                 logout
                                 )
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404

from .forms import UserLoginForm, UserRegistrationForm, ProfileForm, UserForm
from .models import User

from django.views.generic.edit import UpdateView,DeleteView
from django.urls import reverse_lazy

def index(request):
    return render(request,'index.html')

def contact(request):
    return render(request,'contact.html')

def pro(request):
    query_reslut=User.objects.all()
    context={'result':query_reslut}
    return render(request,'pro.html',context)

def register_view(request):  # Creates a New Account & login New users
    # in_use=User.objects.latest('account_no')
    if request.user.is_authenticated:
        return redirect("home")
    else:
        title = "Create a Bank Account"
        form = UserRegistrationForm(
            request.POST or None,
            request.FILES or None
            )

        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get("password1")
            user.set_password(password)
            user.save()
            new_user = authenticate(email=user.email, password=password)
            login(request, new_user)
            messages.success(
                request,
                '''Thank You For Creating A Bank Account {}.
                Your Account Number is {}, Please use this number to login
                '''.format(new_user.full_name, new_user.email))

            return redirect("index")

        context = {"title": title, "form": form}

        return render(request, "form.html", context)

def login_view(request):  # users will login with their Email & Password
    if request.user.is_authenticated:
        return redirect("home")
    else:
        title = "Load Account Details"
        form = UserLoginForm(request.POST or None)

        if form.is_valid():
            emaill = form.cleaned_data.get("email")
            # user_obj = User.objects.filter(email=emaill).first()
            password = form.cleaned_data.get("password")
            # authenticates Email & Password
            user = authenticate(email=emaill, password=password)
            login(request, user)
            messages.success(request, 'Welcome' )
            return redirect("profile")

        context = {"form": form,
                   "title": title
                   }

        return render(request, "form.html", context)


def logout_view(request):  # logs out the logged in users
    if not request.user.is_authenticated:
        return redirect("login")
    else:
        logout(request)
        return redirect("index")

def profile(request):

    user = request.user
    message = ""

    current_info = {
        'username': user.username,
        'first_name': user.full_name,
        'last_name': user.last_name,
        'email': user.email,
    }

    # return HttpResponse("this is the user profile page for username '%s'. update first, last, email, username, and password here." % request.user.username)
    if request.method == 'POST':

        # create a form instance and populate it with data from the request
        form = ProfileForm(request.POST)

        if form.is_valid():

            if form.cleaned_data['username'] != user.username:
                user.username = form.cleaned_data['username']

            if form.cleaned_data['full_name'] != user.full_name:
                user.full_name = form.cleaned_data['full_name']

            if form.cleaned_data['last_name'] != user.last_name:
                user.last_name = form.cleaned_data['last_name']

            if form.cleaned_data['email'] != user.email:
                user.email = form.cleaned_data['email']

            if form.cleaned_data['password'] != user.password and form.cleaned_data['password'] != "":
                user.set_password(form.cleaned_data['password'])

            user.save()
            message += "Profile updated."

            return render(request, 'disp.html', {'form': form, 'message': message})

    else:
        form = ProfileForm(current_info)

    return render(request, 'disp.html', {'form': form})

class UserUpdate(UpdateView):
    model = User
    form_class = UserForm
    # Setting returning URL
    success_url = reverse_lazy('profile')
    
class UserDelete(DeleteView):
    model = User
    # Setting returning URL
    success_url = reverse_lazy('profile')