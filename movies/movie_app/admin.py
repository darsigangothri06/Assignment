from django.contrib import admin
from .models import Genres, Movie, Collections

# registering models
admin.site.register(Genres)
admin.site.register(Movie)
admin.site.register(Collections)