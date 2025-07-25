


# Standard
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import render
from django.urls import reverse
from .create_profiles import install_user_profiles


# Maths
import random

# Authentication
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Database
from django.db import IntegrityError
from datetime import date
from doodle_app.models import *


# File Handling
from django.core.files.storage import default_storage
from django.core.exceptions import SuspiciousFileOperation
import re
import os

# Define Users to Create
user_set = ["pepe", "turkle", "sheela", "bowfren", "looda", "smol", "sparra", "zoe"]   
doodle_db_users = [
        {"username":"pepe", "email": "pepe@mail.com", "password": "passw0rd"},
        {"username":"turkle", "email": "turkle@mail.com", "password": "passw0rd"},
        {"username":"sheela", "email": "sheela@mail.com", "password": "passw0rd"},
        {"username":"bowfren", "email": "bowfren@mail.com", "password": "passw0rd"},
        {"username":"looda", "email": "looda@mail.com", "password": "passw0rd"},
        {"username":"smol", "email": "smol@mail.com", "password": "passw0rd"},
        {"username":"sparra", "email": "sparra@mail.com", "password": "passw0rd"},
        {"username":"zoe", "email": "zoe@mail.com", "password": "passw0rd"},   
    ]



def db_admin(request):
    return render(request, "doodle_db/db_admin.html")

def insert_categories(request):
    categories = [
        {"name":"people", "description":"Hoomas thinkking they're big special"},
        {"name":"animals", "description":"Lots of differet critters"},
        {"name":"places", "description":"All diffenent kinds of places"},
        {"name":"mechatech","description":"Machines, science and technology"}
    ]
    for cat in categories:
        # Create New Instance of text Post
        new_cat = Category(name = cat["name"],
        description = cat["description"],
                        )
        new_cat.save()

        
def insert_subcategories(request):
    subcategoris  = [
        {"category":"people", }
    ]
    # iterate through the categories
    # foreach category get that instance. This is the foreign key for the subcategory

def insert_static(request):
    try:
        insert_categories(request)
        message="Success, Static Data Inserted: Category"
    except:
        message="Failed to Insert Static Data: Category"
    return render(request, "doodle_db/db_admin.html", {"message":message})
    
    
def delete_static(request):
    Category.objects.all().delete()
    message="Static Data Deleted: Category"
    return render(request, "doodle_db/db_admin.html", {"message":message})




def reset_su(request):
    # Delete existing superuser (optional, if you want to ensure only one exists)
    User.objects.filter(username="doodle_boss").delete()
    
    # Create new superuser
    new_su_user = User.objects.create_superuser(
        username="doodle_boss",
        email="jeferzzone@gmail.com",
        password="Passw0rd"
    )
    # No need to set is_staff or is_superuser, create_superuser handles this
    new_su_user.save()  # Not strictly necessary, as create_superuser saves the user
    
    return render(request, "doodle_db/db_admin.html", {"message": "Superuser Reset"})

        
def insert_users(request):
    # Delete All Curent Users 
    for name in user_set:
        try:
            User.objects.get(username=name).delete() 
        except:
            pass
    
    # Create The New Users
    for user in doodle_db_users:
        new_user = User.objects.create_user(user["username"], user["email"], user["password"])
        new_user.save()

    install_user_profiles(doodle_db_users)
    return render(request,"doodle_db/db_admin.html", {"message":"Users Created"})
        
def delete_users(request):
    # User.objects.all().delete()
    # Delete all but the chief su
    for user in doodle_db_users: # The auto-installed user
        user_name = user["username"]
        try:
            User.objects.get(username = user_name).delete()
        except:
            print(f"user {user_name} Does not exist")
       
    User.objects.all().delete() # Everyone including doodle_boss

    #User_Post.objects.all().delete()
    #User_Profile.objects.all().delete()
    #Engagement_m2m.objects.all().delete()

    return render(request, "doodle_db/db_admin.html", {"message":"All Data Deleted"})




def inactive(request):
    return render(request, "doodle_db/db_admin.html", {"message":"Button Inactive"})
