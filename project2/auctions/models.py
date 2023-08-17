from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    watchlist = models.ManyToManyField('AuctionListing', blank=True, related_name="users_watching")

    def __str__(self):
        return f"{self.username}"
    
class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"

class AuctionListing(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    open = models.BooleanField(default=True)
    title = models.CharField(max_length=128)
    description = models.TextField() 
    image = models.CharField(max_length=128, default='')
    currentPrice = models.IntegerField()
    currentBid = models.ForeignKey('Bid', on_delete=models.DO_NOTHING, related_name="listing", null=True)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, related_name="listings")
    creationDate = models.DateTimeField(default=timezone.now, blank=True)

    def __str__(self):
        return f"{self.title} | Price: {self.currentPrice}"

class Bid(models.Model):
    id = models.AutoField(primary_key=True)
    auction = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="bids")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    value = models.IntegerField()
    creationDate = models.DateTimeField(default=timezone.now, blank=True)

    def __str__(self):
        return f"Bid in {self.auction.title} of ${self.value} made by {self.user.username}"

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    auction = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    creationDate = models.DateTimeField(default=timezone.now, blank=True)

    def __str__(self):
        return f"{self.text} | Created on {self.creationDate}"