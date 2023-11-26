from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from django.db import models
from main_app.managers import AuthorManager


# Create your models here.
class Author(models.Model):
    full_name = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(limit_value=3)]
    )
    email = models.EmailField(unique=True)
    is_banned = models.BooleanField(default=False)
    birth_year = models.PositiveIntegerField(
        validators=[MinValueValidator(limit_value=1900),
                    MaxValueValidator(limit_value=2005)]
    )
    website = models.URLField(blank=True, null=True)

    objects = AuthorManager()


class Article(models.Model):
    CATEGORY_CHOISES = (
        ('Technology', 'Technology'),
        ('Science', 'Science'),
        ('Education', 'Education')
    )
    title = models.CharField(
        max_length=200,
        validators=[MinLengthValidator(limit_value=5)]
    )
    content = models.TextField(
        validators=[MinLengthValidator(limit_value=10)]
    )
    category = models.CharField(
        max_length=10,
        choices=CATEGORY_CHOISES,
        default='Technology'
    )
    authors = models.ManyToManyField(to=Author, related_name='authors_article')
    published_on = models.DateTimeField(auto_now_add=True,
                                        editable=False)


class Review(models.Model):
    content = models.TextField(
        validators=[MinLengthValidator(limit_value=10)]
    )
    rating = models.FloatField(
        validators=[MinValueValidator(limit_value=1.0),
                    MaxValueValidator(limit_value=5.0)]
    )
    author = models.ForeignKey(to=Author, on_delete=models.CASCADE, related_name="author_review")
    article = models.ForeignKey(to=Article, on_delete=models.CASCADE, related_name="article_review")
    published_on = models.DateTimeField(auto_now_add=True, editable=False)
