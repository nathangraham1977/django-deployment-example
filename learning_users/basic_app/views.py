from django.shortcuts import render
from basic_app.forms import UserForm, UserProfileInfoForm


#for login functionality
from django.contrib.auth import authenticate, login,logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
#will be used as a decorator - can be used in any view that requires the user to be logged in
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    return render(request,'basic_app/index.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

@login_required
def special(request):
    return HttpResponse("You are logged in, Nice!")

def register(request):

    registered = False

    if request.method == "POST":

        #using two forms because of us allowing the user to upload a file/Imageself
        #Hence the enctype="multipart/form-data" value on the registration.html source code

        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            registered = True

        else:
            print(user_form.errors, profile_form.errors)

    else:
        #user has not submitted any data on the form, it should show the "blank forms"

        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request, 'basic_app/registration.html',
                    {'user_form': user_form,
                     'profile_form': profile_form,
                     'registered': registered})

def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)

        if user:
            login(request,user)
            return HttpResponseRedirect(reverse('index'))

        else:
            print("Someone tried to login and failed")
            return HttpResponse("invalid login details supplied")
    else:
        return render(request, 'basic_app/login.html',{})
