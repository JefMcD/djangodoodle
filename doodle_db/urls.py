
from django.urls import path
from django.urls import re_path
from . import views, db_admin

app_name = "doodle_db"
urlpatterns = [
    # db_admin paths
    path("", db_admin.db_admin, name="db_admin"),
    path("insert_users", db_admin.insert_users, name="insert_users"),
    path("reset_su", db_admin.reset_su, name="reset_su"),
    path("insert_static", db_admin.insert_static, name="insert_static"),
    path("delete_static", db_admin.delete_static, name="delete_static"),
    path("inactive", db_admin.inactive, name="inactive"),
    path("delete_users", db_admin.delete_users, name="delete_users"),
    


]