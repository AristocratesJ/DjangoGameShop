import datetime

from django.db import models
from django.contrib.auth.models import User


class Game(models.Model):
    PLATFORM_CHOICES = [
        ('PS', 'PlayStation'),
        ('XB', 'Xbox'),
        ('PC', 'PC'),
        ('NT', 'Nintendo'),
    ]

    name = models.CharField(max_length=200)
    developer = models.ForeignKey('Developer', on_delete=models.CASCADE)
    add_date = models.DateField(default=datetime.date.today)
    rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    platform = models.CharField(max_length=2, choices=PLATFORM_CHOICES)
    image = models.ImageField(upload_to='images/games/', blank=True, null=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.name

class Developer(models.Model):
    name = models.CharField(max_length=200)
    website = models.URLField()

    def __str__(self):
        return self.name

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'game')

    def __str__(self):
        return f"Cart's item: {self.game}, price: {self.game.price}"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username} created at {self.created_at}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.game} for {self.order}"


