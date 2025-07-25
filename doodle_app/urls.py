

from django.urls import path
from django.urls import re_path
from . import views

app_name = "doodle_app"
urlpatterns = [
    # Authenticate views paths
    path("", views.entry, name='entry'),
    path("signin", views.signin, name="signin"),
    path("join", views.join, name="join"),
    path("reset_password", views.reset_password, name="reset_password"),
    path("signout", views.signout, name="signout"),
    path("add_user", views.add_user, name="add_user")
    
    #path("unsplash_api_test", views.unsplash_api_test, name="unsplash_api_test"),
    


]



