from django.shortcuts import render

from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .models import Task, User
from .forms import TaskForm,CustomUserCreationForm

# home
def home(request):
    return render(request, 'app1/home.html')


def sign_up(request):
    if request.method == 'POST':
        fm = CustomUserCreationForm(request.POST)
        if fm.is_valid():
            fm.save()
            return HttpResponseRedirect('/login/')
    else:
        fm = CustomUserCreationForm()
    return render(request, 'app1/signup.html', {'form': fm})


def ulogin(request):
    if request.method == 'POST':
        print("Request Data-----------------> ", request.POST)
        fm = AuthenticationForm(request=request, data=request.POST)
        print("fm is Valid ----------------->",fm.is_valid())
        if fm.is_valid():
            print("fm is Valid ----------------->",fm.is_valid())
            # Use the correct field to get the email
            uemail = fm.cleaned_data['username']
            upass = fm.cleaned_data['password']
            
            user = authenticate(email=uemail, password=upass)  # Use the email field for authentication
            
            if user is not None:
                login(request, user)
                if user.is_superuser:
                    # Redirect superusers to a different URL
                    return HttpResponseRedirect('/error/')
                return HttpResponseRedirect('/profile/')
    
    else:
        fm = AuthenticationForm()
    
    return render(request, 'app1/login.html', {'form': fm})
    #if request.method == 'POST':
    #    print("RRRRRRRRRR", request)
    #    fm = AuthenticationForm(request=request, data=request.POST)
    #    print("fm",fm.is_valid())
    #    if fm.is_valid():
    #        print("fmaaaaaaaaaaaaaaaa",fm.is_valid())
    #        
    #        uemail = fm.cleaned_data['username']
    #        upass = fm.cleaned_data['password']
    #        print("uemail,upass",uemail,upass)
    #        user = authenticate(email=uemail, password=upass)
    #        
    #        if user is not None:
    #            if user.is_superuser == False:
    #                login(request, user)
    #                return HttpResponseRedirect('/profile/')
    #            return render(request, 'app1/login.html', {'form': fm})
    #else:
    #    fm = AuthenticationForm()
    #return render(request, 'app1/login.html', {'form': fm})


# User Prfile
def uprofile(request):
    if request.user.is_authenticated:
        #user_tasks = Task.objects.filter(user=request.user) # display sepecific user tasks
        user_tasks = Task.objects.all()
        return render(request, 'app1/profile.html', {'tasks': user_tasks})

    else:
        return HttpResponseRedirect('/login/')


# logout
def ulogout(request):
    logout(request)
    return HttpResponseRedirect('/login/')


# add task
def add_task(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = TaskForm(request.POST)
            if form.is_valid():
                form.instance.user = request.user
                form.save()
                return HttpResponseRedirect('/profile/')
        else:
            form = TaskForm()
        return render(request, 'app1/add_task.html', {'form': form})
    else:
        return HttpResponseRedirect('/login/')
    
    
    
    
def update_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    
    if request.user != task.user:
        return HttpResponseRedirect('/error/')
    
    else:
        if request.method == 'POST':
            form = TaskForm(request.POST, instance=task)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/profile/')
        else:
            form = TaskForm(instance=task)
        return render(request, 'app1/update_task.html', {'form': form, 'task': task})
   
# delete task
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    
    if request.user != task.user:
        return HttpResponseRedirect('/error/')
    else:
        task.delete()
        return HttpResponseRedirect('/profile/')


# view detail of Task
def task_details(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    return render(request, 'app1/task_details.html', {'task': task})

def uerror(request):
    return render(request, 'app1/error.html')