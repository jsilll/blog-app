from django.shortcuts import render, redirect

from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from .models import User

# Create your views here.
def register(request):
    if request.user.is_authenticated:
        return redirect('blog-home')
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            # username = form.cleaned_data.get("username")
            messages.success(request, 'Your account has been created! You are now able to login.')
            return redirect('login')
        else:
            form = UserRegisterForm()
            return render(request, 'users/register.html', context={'form' : form, 'title' : 'register'})
    else:
        form = UserRegisterForm()
        return render(request, 'users/register.html', context={'form' : form, 'title' : 'register'})

@login_required
def profile(request):
    if request.method == 'POST':
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if p_form.is_valid():
            p_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('blog-home')
    else:
        # u_form = UserUpdateForm()
        p_form = ProfileUpdateForm(instance=request.user.profile)
        context = {
            'p_form' : p_form,
        }
        return render(request, 'users/profile.html', context=context)

class UserDetailView(DetailView):
    model = User
    template_name = 'blog/user_detail.html'