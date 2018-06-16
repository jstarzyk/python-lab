from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages


# Create your views here.
from django.views.generic.base import View, RedirectView

from app.forms import RegistrationForm


class HomePageView(TemplateView):
    def get(self, request, **kwargs):
        # return render(request, 'registration/login.html', context=None)
        # return render(request, 'registration/login.html')
        return redirect(to='login/')


class AboutPageView(TemplateView):
    template_name = 'about.html'


class RegisterView(TemplateView):
    template_name = 'registration/register.html'


class StudentView(TemplateView):
    def get(self, request, *args, **kwargs):


        return render(request, 'student.html')


class AddPerson(FormView):
    # form_class = UserCreationForm
    form_class = RegistrationForm
    template_name = 'registration/register.html'
    success_url = '/register/'

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data['username']
        # raw_password = form.cleaned_data.get('password1')
        raw_password = form.cleaned_data['password1']
        user = authenticate(username=username, password=raw_password)
        login(self.request, user)
        messages.success(self.request, 'Account created successfully')
        # return redirect(to='register/')
        return super().form_valid(form)

    # class Meta:
    #     model

# class AddPerson(TemplateView):
#     template_name = 'registration/register.html'
#
#     def post(self, request, **kwargs):
#         f = UserCreationForm(request.POST)
#         if f.is_valid():
#             f.save()
#             messages.success(request, 'Account created successfully')
#             return redirect('register')
# return render(request, 'registration/register.html', {'form': f})
