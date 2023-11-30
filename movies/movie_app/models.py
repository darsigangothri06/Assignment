from django.db import models
from django.contrib.auth.models import User
import uuid # to get unique id

class Genres(models.Model):
    genres_name = models.CharField(primary_key = True, max_length=100) 

class Movie(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=400)
    genres = models.ManyToManyField(Genres, null=True)
    uuid = models.UUIDField(primary_key=True)

class Collections(models.Model):
    uuid = models.UUIDField(primary_key=True, default = uuid.uuid4)
    title = models.CharField(max_length=100)
    movies = models.ManyToManyField(Movie)
    description = models.CharField(max_length=50)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)