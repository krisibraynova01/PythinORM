from django.core.validators import MinLengthValidator, MaxLengthValidator, MinValueValidator, MaxValueValidator
from django.db import models
from main_app.managers import DirectorManager


# Create your models here.
class Director(models.Model):
    full_name = models.CharField(
        max_length=120,
        validators=[MinLengthValidator(limit_value=2),
                    MaxLengthValidator(limit_value=120)]

    )
    birth_date = models.DateField(default='1900-01-01')
    nationality = models.CharField(
        max_length=50,
        default='Unknown'
    )
    years_of_experience = models.SmallIntegerField(
        validators=[MinValueValidator(limit_value=0)],
        default=0
    )

    objects = DirectorManager()


class Actor(models.Model):
    full_name = models.CharField(
        max_length=120,
        validators=[MinLengthValidator(limit_value=2),
                    MaxLengthValidator(limit_value=120)]

    )
    birth_date = models.DateField(default='1900-01-01')
    nationality = models.CharField(
        max_length=50,
        default='Unknown'
    )
    is_awarded = models.BooleanField(default=False)
    last_updated = models.DateTimeField(auto_now=True)


class Movie(models.Model):
    GENRE_CHOISES = (
        ('Action', 'Action'),
        ('Comedy', 'Comedy'),
        ('Drama', 'Drama'),
        ('Other', 'Other')
    )
    title = models.CharField(
        max_length=150,
        validators=[MinLengthValidator(limit_value=5),
                    MaxLengthValidator(limit_value=150)]
    )
    release_date = models.DateField()
    storyline = models.TextField(null=True, blank=True)
    genre = models.CharField(max_length=6,
                             choices=GENRE_CHOISES, default='Other')
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        default=0.0,
        validators=[MinValueValidator(limit_value=0.0),
                    MaxValueValidator(limit_value=10.0)]
    )
    is_classic = models.BooleanField(default=False)
    is_awarded = models.BooleanField(default=False)
    last_updated = models.DateTimeField(auto_now=True)
    director = models.ForeignKey(to=Director, on_delete=models.CASCADE, related_name="director_movies")
    starring_actor = models.ForeignKey(to=Actor,
                                       null=True,
                                       on_delete=models.SET_NULL, related_name="starring_actor_movies")
    actors = models.ManyToManyField(to=Actor, related_name="actor_movies")
