from django.db import models

# Create your models here.
# All SQL Tables models


class feedbacks(models.Model):
    DateTime = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=50)
    text = models.TextField()
    bw = models.CharField(max_length=4)
    objects = models.Manager()


class analyzedFeedbacks(models.Model):
    fid = models.IntegerField(primary_key=True)
    DateTime = models.DateTimeField()
    category = models.CharField(max_length=50)
    text = models.TextField()
    bw = models.CharField(max_length=4)
    related = models.IntegerField(blank=True, null=True)
    objects = models.Manager()


class wish(models.Model):
    fid = models.IntegerField(primary_key=True)
    text = models.TextField()
    category = models.CharField(max_length=50)
    related = models.IntegerField(blank=True, null=True)
    objects = models.Manager()


class democratic(models.Model):
    fid = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    category = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    dueDate = models.DateField()
    filePath = models.FileField(
        upload_to='democratic/', blank=True, null=True)
    pvotes = models.IntegerField(blank=True, default=0)
    nvotes = models.IntegerField(blank=True, default=0)
    objects = models.Manager()


class account(models.Model):
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    Nr = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    zipCode = models.CharField(max_length=255)
    dob = models.CharField(max_length=255)
    email = models.EmailField(max_length=254)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    objects = models.Manager()

# hvgh


class game(models.Model):
    imagePath = models.ImageField(upload_to='game/')
    a = models.CharField(max_length=255)
    b = models.CharField(max_length=255)
    c = models.CharField(max_length=255)
    d = models.CharField(max_length=255)
    right = models.CharField(max_length=255)
    objects = models.Manager()


class related(models.Model):
    followed = models.IntegerField(blank=True, null=True)
    follower = models.IntegerField(blank=True, null=True)
    objects = models.Manager()
