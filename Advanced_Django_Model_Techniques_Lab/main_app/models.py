from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator, MinValueValidator, MaxValueValidator
from django.db import models


# Create your models here.

class Restaurant(models.Model):
    name = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(2, message="Name must be at least 2 characters long."),
                    MaxLengthValidator(100, message="Name cannot exceed 100 characters.")])
    location = models.CharField(
        max_length=200,
        validators=[MinLengthValidator(2, message="Location must be at least 2 characters long."),
                    MaxLengthValidator(200, message="Location cannot exceed 200 characters.")]
    )
    description = models.TextField(blank=True,
                                   null=True)
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        validators=[MinValueValidator(0, message="Rating must be at least 0.00."),
                    MaxValueValidator(5, message="Rating cannot exceed 5.00.")]
    )


class Menu(models.Model):
    def validate_menu_categories(value):
        needed_categories = ["Appetizers", "Main Course", "Desserts"]

        for category in needed_categories:
            if category.lower() not in value.lower():
                raise ValidationError(
                    'The menu must include each of the categories "Appetizers", "Main Course", "Desserts".')

    name = models.CharField(
        max_length=100
    )
    description = models.TextField(
        validators=[validate_menu_categories]
    )
    restaurant = models.ForeignKey(to=Restaurant,
                                   on_delete=models.CASCADE)


class ReviewMixin(models.Model):
    rating = models.PositiveIntegerField(
        validators=[MaxValueValidator(limit_value=5)]
    )
    review_content = models.TextField()

    class Meta:
        abstract = True
        ordering = ['-rating']


class RestaurantReview(ReviewMixin):
    reviewer_name = models.CharField(
        max_length=100
    )
    restaurant = models.ForeignKey(to=Restaurant,
                                   on_delete=models.CASCADE
                                   )
    review_content = models.TextField()
    rating = models.PositiveIntegerField(
        validators=[MaxValueValidator(limit_value=5)]
    )

    class Meta(ReviewMixin.Meta):
        ordering = ['-rating']
        verbose_name = 'Restaurant Review'
        verbose_name_plural = 'Restaurant Reviews'
        unique_together = ['reviewer_name', 'restaurant']

        abstract = True


class RegularRestaurantReview(RestaurantReview):
    pass


class FoodCriticRestaurantReview(RestaurantReview):
    food_critic_cuisine_area = models.CharField(max_length=100)

    class Meta(RestaurantReview.Meta):
        ordering = ['-rating']
        verbose_name = 'Food Critic Review'
        verbose_name_plural = 'Food Critic Reviews'
        unique_together = ['reviewer_name', 'restaurant']


class MenuReview(ReviewMixin):
    reviewer_name = models.CharField(max_length=100)
    menu = models.ForeignKey(to=Menu,
                             on_delete=models.CASCADE)
    review_content = models.TextField()
    rating = models.PositiveIntegerField(
        validators=[MaxValueValidator(limit_value=5)]
    )

    class Meta(ReviewMixin.Meta):
        ordering = ['-rating']
        verbose_name = "Menu Review"
        verbose_name_plural = "Menu Reviews"
        unique_together = ['reviewer_name', 'menu']
        indexes = [models.Index(fields=['menu'],
                                name="main_app_menu_review_menu_id")]
