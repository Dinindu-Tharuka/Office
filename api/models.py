from django.db import models
from django.conf import settings
from core.models import User

class Job(models.Model):
    job_title = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.job_title

class Sector(models.Model):
    sector_title = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.sector_title

class City(models.Model):
    city_title = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.city_title

class District(models.Model):
    district_title = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.district_title

class Province(models.Model):
    province_title = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.province_title

class Category(models.Model):
    category_title = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.category_title

class Client(models.Model):

    ## Gender Choices

    GENDER_FEMALE = 'F'
    GENDER_MALE = 'M'
    GENDER_OTHER = 'O'
    SELECT = 'S'

    GENDER_CHOICES = [
        (SELECT, 'Select'),
        (GENDER_FEMALE, 'Female'),
        (GENDER_MALE, 'Male'),
        (GENDER_OTHER, 'Other')
    ]

    ## Is Sri lanaka

    IS_SRI_LANKA = 'S'
    OTHER ='O'

    SRI_LANAKA_CHOICES = [
        (SELECT, 'Select'),
        (IS_SRI_LANKA, 'Sri Lanka'),
        (OTHER, 'Other'),
    ]
    # first_name = models.CharField(max_length=50)
    # last_name = models.CharField(max_length=50, null=True, blank=True)
    number = models.CharField(max_length=20, null=True, blank=True)
    nic = models.CharField(max_length=20, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    date_of_issue = models.DateField(null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default=SELECT, null=True, blank=True)
    precent_working_place = models.CharField(max_length=255, null=True, blank=True)
    photo = models.ImageField(upload_to='photos/')
    is_sri_lanka = models.CharField(max_length=1, choices=SRI_LANAKA_CHOICES, default=SELECT, null=True, blank=True)
    remark = models.CharField(max_length=50, null=True, blank=True)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='clients', null=True, blank=True)
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE, related_name='clients', null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='clients', null=True, blank=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='clients', null=True, blank=True)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='clients', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='clients', null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    

    
    
