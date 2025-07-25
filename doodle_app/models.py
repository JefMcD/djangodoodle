from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import URLValidator
from django.db.models.signals import post_delete, pre_delete
from django.dispatch.dispatcher import receiver
from django.conf import settings
import os


# Create your models here.


# Custom User (fields added to the Django user model)
class User(AbstractUser):
    #  For Authentication
    # Has One to One relation with User_Profile
    username            = models.CharField(max_length=150, unique=True)
    firstname           = models.CharField(null=False, blank=False, max_length=16)
    lastname            = models.CharField(null=False, blank=False, max_length=16)
    email               = models.EmailField(max_length=254, unique=False, null=True, blank=True)
    password            = models.CharField(max_length=128)

    # email unique = False for dev only. set to True for production
    def __str__(self):
        return f"{self.pk}, {self.username}, {self.email}"

# There is a One To One relationship between User_Profile and User
class User_Profile(models.Model):
    id                  = models.AutoField(primary_key=True, db_index=True)
    user_id_121         = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    bio                 = models.TextField(blank=True, null=True)
    caption             = models.CharField(null=True, blank=True, max_length=50)
    avatar              = models.ImageField(null=True, blank=True, upload_to="user_avatars")
    is_premium          = models.BooleanField(default=False)
    favorite_pics_m2m   = models.ManyToManyField("doodle_app.Picture", blank=True, related_name='users_who_faved_set') # Creates a list of a users favorite pics for future sessions
    dropped_pics_m2m    = models.ManyToManyField("doodle_app.Picture", blank=True, related_name = 'users_who_dropped_set') # For when you want to exclude a picture from future sessions
    follows             = models.ManyToManyField('self', symmetrical=False, related_name='followers') # possible future
    mutes               = models.ManyToManyField('self', symmetrical=False, related_name='muters')      # future
    blocks              = models.ManyToManyField('self', symmetrical=False, related_name='blockers')    # future
   
    def __str__(self):
        return f"{self.pk}, {self.id}"
    
class Post(models.Model):
    # I confirm that this is my art, made by my warm little paw and not by AI
    pass
    
# Music
class Music(models.Model):
    id          = models.AutoField(primary_key=True)
    name        = models.CharField(max_length=100, blank=True, null=True)
    music_file  = models.FileField(upload_to='music/')
    description = models.TextField(blank=True, null=True)
    icon        = models.ImageField(null=True, blank=True, upload_to="icons_music")

    def __str__(self):
        return self.name or f"Music {self.id}"


    
# Mode the Practice Mode
class Practice_Mode(models.Model):
    MODE_CHOICES = [
        ('warm_up', 'Warm-Up'),         #(value stired in CharField, human readable label for forms)
        ('doodle_dash', 'Doodle Dash'),
        ('katasketch', 'Katasketch'),
    ]
    id              = models.AutoField(primary_key=True)
    mode_name       = models.CharField(max_length=20, choices=MODE_CHOICES)
    duration_sec    = models.IntegerField(help_text="Total duration of this mode in seconds")

    @property
    def total_pictures(self):
        return sum(interval.number_of_pics for interval in self.intervals.all())
    # called using -> print(drawing_mode.total_pictures)
    
    # Expose Drill info through Practice_Mode (for frontend)
    # Create a @property on Practice_Mode or Practice_Time that returns a JSON-like list 
    # # of all Drills for quick serialization.
    # You need to do this with Django DRF so leaveit for now - get the basics done first


    def __str__(self):
        return f"{self.get_mode_name_display()} - {self.duration_sec // 60} min"
    
    
# The times for each Drill
# Practice_Time = A preset or custom config for how a Practice_Mode behaves (timings, freestyles).
class Practice_Time(models.Model):
    id                  = models.AutoField(primary_key=True)
    practice_mode_fk    = models.ForeignKey(Practice_Mode, on_delete=models.CASCADE, null=False, related_name="set_of_times")    
    durations_secs      = models.IntegerField(help_text="The total duration of the practice")
    is_freestyle        = models.BooleanField(default=False)
    label               = models.CharField(max_length=45, blank=True, null=True)
  
    
    
    
# The picture time combinations for each Practice Time
class Drill(models.Model):
    id               = models.AutoField(primary_key=True)
    practice_time_fk = models.ForeignKey(Practice_Time, on_delete=models.RESTRICT, null=False)
    number_of_pics   = models.IntegerField(help_text="the number of pics to be displayed")
    display_time     = models.IntegerField(help_text="the number of seconds a picture is displayed")
    step_order   = models.IntegerField(help_text="The position od this squence in the order")


























class Image_API(models.Model): # The Api used to fetch the pictures
    PICTURE_SOURCES = [
        ('sketch_draw_doodle', 'Sketch Draw Doodle'),
        ('unsplash', 'Unsplash'),
        ('public_domain_pictures', 'Public Domain Pictures'),
        ('pixabay', 'Pixabay'),
        ('gratisography', 'Gratisography'),
        ('user_pics', 'User Upload')
    ]
    id              = models.AutoField(primary_key=True)
    source_name     = models.CharField(max_length=45, choices=PICTURE_SOURCES)
    source_url      = models.URLField()
    api_key         = models.CharField(max_length=255)
    api_pass        = models.CharField(max_length=32)
    # Sensitive API data needs to be held in the .env file. Could be risky for them to be held in the database and definitely not in the client
    # I'll need to do some decpouple magic with this or somethin fancy
    
    def __str__(self):
        return f"id: {self.id}, Picture Source {self.picture_source}" 
  


# Category
class Category(models.Model):
    id          = models.AutoField(primary_key=True)
    name        = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    icon        = models.ImageField(null=True, blank=True, upload_to="icons_category")

    def __str__(self):
        return self.name

# Subcategory
class Subcategory(models.Model):
    id           = models.AutoField(primary_key=True)
    category_fk  = models.ForeignKey(Category, on_delete=models.RESTRICT, null=True)
    name         = models.CharField(max_length=100)
    icon         = models.ImageField(null=True, blank=True, upload_to="icons_subcategory")
    description  = models.TextField(blank=True, null=True)


    def __str__(self):
        return self.name

# Tag
class Tag(models.Model):
    id              = models.AutoField(primary_key=True)
    tagname         = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name



# This is the list of all pictures in the database
# there is a Many To Many relation between Picture and Picture Set
class Picture(models.Model):
    id              = models.AutoField(primary_key=True)
    name            = models.CharField(max_length=100)
    description     = models.TextField(blank=True, null=True)
    image           = models.ImageField(upload_to="pictures")
    picture_api_fk  = models.ForeignKey(Image_API, on_delete=models.RESTRICT, null=False) # The id of the picture on the api eg the unsplash id of the picture
    category_fk     = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='pictures', null=False)
    subcategory_fk  = models.ForeignKey(Subcategory, on_delete=models.CASCADE, related_name='pictures', null=False)
    picTags_m2m     = models.ManyToManyField(Tag, blank=True) # Unused for now may delete this attribute late
    hotlink_url     = models.URLField()
    
    photographer    = models.CharField(max_length=100, blank=True, null=True)
    is_premium      = models.BooleanField(default=False)
    is_ai           = models.BooleanField(default=False) # was the image created by AI

 
    def __str__(self):
        return self.name or f"Picture {self.id}"



# -----------------------------------
# PICTURE SET The set of pictures for the session
# -----------------------------------
class Picture_Set(models.Model):
    id                  = models.AutoField(primary_key=True)
    picture_Set_m2m     = models.ManyToManyField(Picture, through='doodle_app.Picture_Set_m2m')
    category_fk         = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    subcategories_m2m   = models.ManyToManyField(Subcategory)
    saved_at            = models.BooleanField(default=False)
    created_at          = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Picture_Set {self.id} by {self.created_by}"

    

    
# Session
# A User creates a Session  which has a Picture Set, A Music Choice and a Time Mode
# There is a One To One relation between Session and Picture Set
class Session(models.Model):
    id                  = models.AutoField(primary_key=True)
    user_profile_fk     = models.ForeignKey(User_Profile, on_delete=models.RESTRICT)
    music_fk            = models.ForeignKey(Music, on_delete=models.SET_NULL, null=True)
    practice_mode_m2m   = models.ManyToManyField(Practice_Mode, through="Practice_Mode_m2m")

    def __str__(self):
        return f"Session {self.id} by {self.user_profile_fk}"
    
    
    
# The number of pictures and how long they should be displayed
# For each Practice_Mode
# Practice_Mode_m2m says: "In this session, we’ll run this Practice_Mode using this specific Practice_Time with this Picture_Set."
class Practice_Mode_m2m(models.Model):
    session_fk          = models.ForeignKey(Session, on_delete=models.CASCADE, null=False, related_name="unused1")
    practice_mode_fk    = models.ForeignKey(Practice_Mode, on_delete=models.CASCADE, null=False, related_name="unused2")
    practice_time_fk    = models.ForeignKey(Practice_Time, on_delete=models.CASCADE, null=False, related_name="unused3")
    picture_set_fk      = models.ForeignKey(Picture_Set, on_delete=models.RESTRICT, related_name="unused4")
    
  # Prevent a session from accidentally having multiple entries for the same mode:
    class Meta:
        unique_together = [('session_fk', 'practice_mode_fk')]

  

# -----------------------------------------
#  Picture_Set_m2m is A custom through table 
#  containing the list of pictures in a Picture_Set 
class Picture_Set_m2m(models.Model):
    id              = models.AutoField(primary_key=True)
    picture_set_fk  = models.ForeignKey(Picture_Set, on_delete=models.CASCADE)
    pictures_fk     = models.ForeignKey(Picture, on_delete=models.CASCADE)
    sequence_pos    = models.IntegerField()
    skipped         = models.BooleanField(default=False)
    added_at        = models.DateTimeField(auto_now_add=True) # Whan pic was added to the Picture_Set
    shown_at        = models.DateTimeField(null=True, blank=True) # When the Pic was displayed
    
    ordering = ['sequence_pos']

    # This prevents duplicate picture entries in the same Picture_Set and ensures sequence_pos is unique within a set:
    class Meta:
        unique_together = [('picture_set_fk', 'sequence_pos'), ('picture_set_fk', 'pictures_fk')]

    def __str__(self):
        return f"id: {self.id}, sequence_pos: {self.sequence_pos}, skipped: {self.skipped}, timestamp: {self.timestamp}"
    


  
  
  
  








# DonationLink
class DonationLink(models.Model):
    id          = models.AutoField(primary_key=True)
    platform    = models.CharField(max_length=50)
    url         = models.URLField(max_length=2083)
    active      = models.BooleanField(default=True)

    def __str__(self):
        return self.platform

# SocialMediaLink
class SocialMediaLink(models.Model):
    id          = models.AutoField(primary_key=True)
    platform    = models.CharField(max_length=50)
    url         = models.URLField(max_length=2083)
    icon        = models.CharField(max_length=255, blank=True, null=True)
    active      = models.BooleanField(default=True)

    def __str__(self):
        return self.platform



# Simple Serializers
from django.forms.models import model_to_dict

def serialize_instance(instance, fields=None):
    return model_to_dict(instance, fields=fields)

# Example:
# serialize_instance(picture, fields=['id', 'title', 'image'])

