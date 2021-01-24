from django.shortcuts import render
from Apptemp.forms import UserProfileInfoForm, UserForm
from django.contrib.auth.models import User


# Imports for user logins:
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout




# Create your views here.

def index(request):
    context_dict = {'text':'hello world','number':100}
    return render(request,'Apptemp/index.html', context=context_dict)


def other(request):
    return render(request,'Apptemp/other.html')


def rel_url(request):
    return render(request,'Apptemp/relative_url_templates.html')

def registration(request):

    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()
            user.set_password(user.password)  # This step hashes the password.
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user # This links profile to the original 1-1 relationship.

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            registered = True
        else:
            print(user_form.errors,profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()


    return render(request,'Apptemp/registration.html',context=
                                                    {'user_form':user_form,
                                                    'profile_form':profile_form,
                                                    'registered':registered
                                                    }
                )


def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('home'))

            else:
                return HttpResponse("ACCOUNT NOT ACTIVE")

        else:
            print("Someone tried to login and failed")
            print("Username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details supplied")

    else:
        return render(request, 'Apptemp/login.html',{})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))
