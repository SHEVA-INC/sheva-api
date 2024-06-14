from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

from boots.models import Boots


class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField(verbose_name="Review Text")
    rating = models.FloatField(
        verbose_name="Rating",
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)],
        help_text='Choose a rating between 1 and 5'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date Created")

    def __str__(self):
        return f'Review for {self.boots.name} by {self.user.username}'
