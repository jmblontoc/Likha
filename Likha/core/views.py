from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from helpers import user_redirects

# Create your views here.
from django.views import View


class SignInView(View):

    template_name = 'core/login.html'

    def get(self, request):

        if request.user.is_authenticated:
            return user_redirects.redirect_to(request.user)
        return render(request, self.template_name, None)

    def post(self, request):

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return user_redirects.redirect_to(user)

        messages.error(request, 'Invalid credentials')
        return render(request, self.template_name, None)


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)

    return redirect('core:login')