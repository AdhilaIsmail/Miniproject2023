from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, phone, email, role=None, password=None):
        if not email:
            raise ValueError('User must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            phone=phone, 
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,phone, email, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            phone=phone,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractUser):
    DONOR = 1
    HOSPITAL = 2
    STAFF = 3
    REGISTEREDDONOR = 4

    ROLE_CHOICE = (
        (DONOR, 'DONOR'),
        (HOSPITAL, 'HOSPITAL'),
        (STAFF, 'STAFF'),
        (REGISTEREDDONOR, 'REGISTEREDDONOR'),
    )

    username=None
    first_name = None
    last_name = None
    USERNAME_FIELD = 'email'
    email = models.EmailField(max_length=100, unique=True)
    phone = models.CharField(max_length=12, blank=True)
    password = models.CharField(max_length=128)
    role = models.IntegerField(choices=ROLE_CHOICE,default='1')
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superadmin = models.BooleanField(default=False)
    
    
    REQUIRED_FIELDS = ['phone']

    objects = UserManager()

    def _str_(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
    
    def set_hospital_role(self):
        self.role = CustomUser.HOSPITAL
        self.save()

class Donor(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    blood_group = models.CharField(max_length=5)
    place = models.CharField(max_length=100)
    
    
    def __str__(self):
        return self.full_name
    

from django.db import models

class DonorResponse(models.Model):
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    bloodType = models.CharField(max_length=5)
    weight = models.FloatField()
    donorHistory = models.CharField(max_length=3)
    difficulty = models.CharField(max_length=3)
    donated = models.CharField(max_length=3)
    allergies = models.CharField(max_length=3)
    alcohol = models.CharField(max_length=3)
    jail = models.CharField(max_length=3)
    surgery = models.CharField(max_length=3)
    diseased = models.CharField(max_length=3)
    hivaids = models.CharField(max_length=3)
    pregnant = models.CharField(max_length=3, null=True, blank=True)
    child = models.CharField(max_length=3, null=True, blank=True)
    feelgood = models.CharField(max_length=3, null=True, blank=True)

#uploading result into database
from django.db import models


class UploadedFile(models.Model):
    file = models.FileField(upload_to='media/uploads/')

from django.db import models


class HospitalRegister(models.Model):
    hospitalName = models.CharField(max_length=100,unique=True)
    contactPerson = models.CharField(max_length=100)
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    # email = models.EmailField(unique=True)
    # phone = models.CharField(max_length=20)
    location = models.TextField()
    gpsCoordinates = models.CharField(max_length=50)
    ownership = models.CharField(max_length=100)
    hospitalURL = models.URLField(blank=True)
    status = models.CharField(max_length=20, default='Active')
    # password = models.CharField(max_length=128)

    
    def __str__(self):
        return self.hospitalName





# models.py

from django.db import models

class BloodType(models.Model):
    blood_type = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.blood_type
    

class BloodRequest(models.Model):
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    blood_group = models.CharField(max_length=5)
    quantity = models.CharField(max_length=10)
    purpose = models.TextField()
    



