from django.contrib.auth.models import User
from django.db import models


class Employer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employer')
    phone = models.CharField(max_length=22, null=True, blank=True)

    def __str__(self):
        return self.user.username


class Candidate(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='candidate')
    phone = models.CharField(max_length=22, null=True, blank=True)
    academic_formation = models.CharField(max_length=150)
    institution = models.CharField(max_length=150)
    knowledge = models.CharField(max_length=300)
    bio = models.CharField(max_length=400)

    def __str__(self):
        return self.user.username


class Company(models.Model):
    owner = models.ForeignKey('auth.User', null=True, blank=True, on_delete=models.CASCADE, related_name='company')
    catchPhrase = models.CharField(max_length=150)
    about = models.CharField(max_length=400)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class JobAdvertisement(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    requirements = models.CharField(max_length=300)
    desirable = models.CharField(max_length=400)
    payment = models.FloatField()
    company = models.ForeignKey(Company, null=True, blank=True, on_delete=models.CASCADE, related_name='advertisements')
