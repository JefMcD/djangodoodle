# Standard
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import redirect
import random

# email
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.utils.html import format_html

import re

# Authentication
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Database
from django.db import IntegrityError
from .models import *

# File Handling
from django.core.files.storage import default_storage
from django.core.exceptions import SuspiciousFileOperation
import os

# Forms
from django.views.decorators.csrf import csrf_exempt
from .forms import *

# Image Handling
from PIL import Image
from django.core.files import File
from django.core.files.images import ImageFile


# Create your views here.

# App forms
signin_form = SignInForm()
join_form   = JoinForm()
password_reset_form = PasswordResetForm()
code_verification_form = CodeVerificationForm()
form_error = {
        "signin_error"          : "",
        "join_error"            : "",
        "code_error"            : "",
}
all_forms = {
        "signin_form"           : signin_form,
        "join_form"             : join_form,
        "password_reset_form"   : password_reset_form,
        "code_verification_form": code_verification_form,
}

# Entry
# Determine If the request.user is authenticated
# Return the appropriate context to render either Guest options or Fren options
def entry(request):
    print(f"########## entry #############")
    print("authenticated = ", request.user.is_authenticated)
    print("username = ", request.user.username)
    if (1):
        # Fren context
        # user account section
        # signout section
        pass
    else:
        # Guest context 
        # signin section signin form
        # signin section reset password form
        # join section join form
        pass 
    print("Render main_doodle_app")
    print("active-section: home-section")
    
    # Need to create a dictionary of all the default states for dynamic messages, forms 
    # across all the sections. Then just pass it in as a single context item
    
    form_error["signin_error"]    = ""
    form_error["join_error"]      = ""
    return render(request, "doodle_app/main_doodle_app.html",{
        "active_section"    :"home-section",
        "all_forms"         : all_forms,
        "form_error"        : form_error,
    })
    
    
def signin(request):
    print(f"Singin")
    
    if request.method == "POST":
         # Attempt to sign user in
        user = request.POST["username"]
        pwd = request.POST["password"]
        user = authenticate(request, username=user, password=pwd)       
        
        if user is not None:
            # Login
            print("Valid: redirect to entry")
            login(request, user)
            return redirect("doodle_app:entry")
        else:
            print("invalid signin")
            print("username: ",request.POST["username"])
            all_forms["signin_form"] = SignInForm(request.POST)
            form_error["signin_error"] = "Invalid username/password"
            return render(request, "doodle_app/main_doodle_app.html",{
                "all_forms"         : all_forms,
                "form_error"        : form_error,
                "active_section"    : "signin-section",
            })
    else:
        form = SignInForm()
        return render(request,"doodle_app:entry",{
            "all_forms"         : all_forms,
            "form_error"        : form_error,
            "active-section"    :"signin-section",
        })
    
    
    
    

def email_confirmation_code(email, code):
    subject = "%d Sketch Draw Doodle Verify"%code
    sender = "alfie@sketchdrawdoodle.com"
    to_list = [email]

    # Plain-text version (fallback)
    text_content = (
        "Please confirm this is the right address for your new account.\n"
        f"Your verification code is: {code}\n"
        "Verification codes expire after two hours.\n\n"
        "Thanks,\nAlfie"
    )

    # HTML version with bold and large code
    html_content = f"""
        <html>
        <body style="font-family: sans-serif; font-size: 16px; color: #333;">
            <p>There’s one quick step you need to complete before creating your Sketch Draw Doodle account.</p>
            <p>Please enter the following verification code:</p>
            <p style="font-size: 32px; font-weight: bold; color: #2a9d8f;">{code}</p>
            <p>This code will expire after two hours.</p>
            <br>
            <p>Thanks,<br>Alfie</p>
        </body>
        </html>
    """

    msg = EmailMultiAlternatives(subject, text_content, sender, to_list)
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def join(request):
    print("################# Join ################")
    if request.method == "POST":
        # process the form
        form = JoinForm(request.POST)
        if form.is_valid():
            # Check if account already exists
            '''
            email_exists = User.objects.filter(email=request.POST["email"]).exists()
            if email_exists:
                print("email exists")
                all_forms["join_form"] = JoinForm(request.POST)
                form_error["join_error"] = "An account with that email Already Exists"
                return render(request, "doodle_app/main_doodle_app.html",{
                    "all_forms"         : all_forms,
                    "form_error"        : form_error,
                    "active_section"    : "join-section",
                })
            '''
            username_exists = User.objects.filter(username=request.POST["username"]).exists()
            if username_exists:
                all_forms["join_form"] = JoinForm(request.POST)
                form_error["join_error"] = "Username already taken"
                return render(request, "doodle_app/main_doodle_app.html",{
                    "all_forms"         : all_forms,
                    "form_error"        : form_error,
                    "active_section"    : "join-section",
                })
            
            # Save user data to session
            user_data =  form.cleaned_data
            request.session["pending_user_data"]=user_data
            
            # Generate random six digit code
            confirmation_code =  random.randint(100000,999999)
            request.session["pending_confirmation_code"] = confirmation_code
            
            # email code to user
            email_confirmation_code(user_data["email"], confirmation_code)

            return render(request, "doodle_app/main_doodle_app.html",{
                "active_section"    :"codeverification-section",
                "all_forms"         : all_forms,
                "form_error"        : form_error,
            })
        else:
            # form invlaid. return form with error
            join_message = "join error"
            print("user details failed validation")
            print("email submitted:", form.data.get("email"))   
            errors = form.errors # dictionary of errors
            # Build a custom error summary (example logic)
            error_messages = []
            errors = form.errors.as_data() #form.errors.as_data() gives you the raw ValidationError objects (not just strings).
            if 'email' in errors:
                for err in errors["email"]:
                    if err.code == "blocked":
                        error_messages.append("Ride Tonto!") # spam error
                    else:
                        error_messages.append("Invalid email address.")
            if 'confirm' in errors:
                error_messages.append("Password or confirmation issue.")
            if 'password' in errors:
                error_messages.append("Password must be min 8 characters and contain, upper case, lower case and numbers.")
            if 'username' in errors:
                error_messages.append("Username unavailable.")

            summary_message = " | ".join(error_messages) or "There was a problem with your submission."

            all_forms["join_form"] = form
            form_error["join_error"] = summary_message          
            return render(request, "doodle_app/main_doodle_app.html",{
                "all_forms"         : all_forms,
                "form_error"        : form_error,
                "active_section"    : "join-section",
            })
    else:
        #Request Method is GET, send blank form and no error
        all_forms["join_form"] = form
        form_error["join_error"] = summary_message          
        return render(request, "doodle_app/main_doodle_app.html",{
            "all_forms"         : all_forms,
            "form_error"        : form_error,
            "active_section"    : "join-section"
        })

def add_user(request):
    # get session data
    code = int(request.POST["verification_code"].strip())
    expected_code = int(request.session.get("pending_confirmation_code"))
    user_data = request.session.get("pending_user_data")
    
    # check code
    if code == expected_code:
        # create the user from stored session data
        # create_user is a special method that automatically saves the instance into the database
        new_user = User.objects.create_user(
            username = user_data["username"],
            password = user_data["password"],
            email = user_data["email"]
        ) 
        # clear session data
        request.session.pop("pending_user_data", None)
        request.session.pop("pending_confirmation_code", None)
        login(request, new_user)
        #return redirect("doodle_app:entry")
        form_message = "Welcome Shinobi! Make yourself at home. This is your sketchbook, you can upload your favorite sketches, drawings and doodles here and share them with your friends"
        return render(request, "doodle_app/main_doodle_app.html",{
            "all_forms"         : all_forms,
            "username"          : user_data["username"],
            "form_error"        : form_error,
            "form_message"      : form_message,
            "active_section"    : "profile-section"
        })
    else:
        print("code bad")
        all_forms["code_verification"] = CodeVerificationForm(request.POST)
        form_error["code_error"] = "Wrong Code"          
        return render(request, "doodle_app/main_doodle_app.html",{
            "all_forms"         : all_forms,
            "form_error"        : form_error,
            "active_section"    : "codeverification-section",
            
            
        })    




def reset_password(request):
    return render(request, "doodle_app/help_page.html")

def signout(request):
    print("sign out")
    logout(request)
    return HttpResponseRedirect(reverse("doodle_app:entry"))

