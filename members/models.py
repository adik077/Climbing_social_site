from django.contrib.auth.models import User
from django.db import models
from taggit.managers import TaggableManager


class UserProfile(models.Model):
    user = models.OneToOneField(User, null=True,blank=True, related_name='userprofile', on_delete=models.CASCADE)
    photo = models.ImageField(null=True,blank=True,upload_to='profile_photos')
    twitter_url = models.CharField(max_length=200, null=True, blank=True)
    facebook_url = models.CharField(max_length=200, null=True, blank=True)
    instagram_url = models.CharField(max_length=200, null=True, blank=True)
    where_from = models.CharField(max_length=200, null=True, blank=True)
    where_lives = models.CharField(max_length=200, null=True, blank=True)
    best_places = TaggableManager(blank=True)
    likes = models.ManyToManyField(User,related_name='user_likes',blank=True,null=True)

    def total_likes(self):
        return self.likes.count

    def __str__(self):
        return str(self.user)








