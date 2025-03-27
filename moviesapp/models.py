from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Tag(models.Model):
    name = models.CharField(max_length=50, verbose_name="Mood tag", unique = True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'


class Movie(models.Model):
    title = models.CharField(max_length=255, unique=True)
    synopsis = models.TextField(verbose_name="Synopsis", default=None, null=True, blank=True)
    release_year = models.IntegerField(null=True, blank=True)
    genre = models.CharField(max_length=100, blank=True)
    director = models.CharField(max_length=255, blank=True)
    cover = models.ImageField('Cover', upload_to='covers/', null=True, blank=True)

    # tmdb_id = models.IntegerField(unique=True, null=True, blank=True)

    def __str__(self):
        return f"{self.title} ({self.release_year})"

class MovieRecommendation(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name="Movie title",related_name='recommendations')
    content = models.TextField(verbose_name="Recommendation description")
    audience = models.TextField(verbose_name="Type of viewer who will enjoy the movie")
    mood = models.TextField(verbose_name="When to watch", null=True, blank=True)
    cherry = models.TextField(verbose_name="Cherry on top", null=True, blank=True, help_text="What was the standout moment for you in the movie? It could be a meaningful line of dialogue, a visually stunning scene, or a moment that resonated with you long after the movie ended") #a quote or visual or whatever sticket out the most for you in the movie
    user = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True)
    tag = models.ManyToManyField(Tag, verbose_name="Mood tag")
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"{self.user.username} recommends {self.movie.title}"

class Comment(models.Model):
    title = models.CharField(max_length=255, verbose_name="Review title", null=True)
    movie = models.ForeignKey(MovieRecommendation, verbose_name="Movie Recommendation", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    content = models.TextField(verbose_name="Text of the review")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    photo = models.ImageField(default="profile_pics/noimage.png", upload_to="profile_pics")

    def __str__(self):
        return f"{self.user.username} profile"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.photo.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.photo.path)