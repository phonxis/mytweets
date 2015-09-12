from django.views.generic import View
from django.conf import settings
from django.shortcuts import render
from django.template import Context
from django.template.loader import render_to_string
from user_profile.forms import RegisterForm
from django.core.mail import EmailMultiAlternatives
from user_profile.models import User
from django.http import HttpResponseRedirect
import hashlib

# Create your views here.
