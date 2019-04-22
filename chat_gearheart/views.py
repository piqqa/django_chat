from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django_registration.forms import RegistrationForm


@login_required#(login_url='accounts/login')
def index(request):
    return render(request, 'chat_gearheart/index.html', {})
