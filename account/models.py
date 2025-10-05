from django.db import models
from django.contrib.auth.models import BaseUserManager , AbstractUser



class CustomUserManager(BaseUserManager):
     
     def create_user(self,email,password=None,**extrafields):
          if not email:
               raise ValueError('The email field must be set')
          
          email = self.normalize_email(email)
          extrafields.setdefault('is_active',True)
          user = self.model(email=email,**extrafields)
          user.set_password(password)
          user.save(using=self._db)
          return user

     def create_superuser(self,email,password=None,**extrafields):
          extrafields.setdefault('is_staff',True)
          extrafields.setdefault('is_superuser',True)

          if extrafields.get('is_staff') is not True:
               raise ValueError('super_user must have is_staff=True')
          if extrafields.get('is_superuser') is not True:
               raise ValueError('super_user must have is_superuser=True')

          return self.create_user(email,password,**extrafields)
     

class User(AbstractUser):
     ROLE_CHOICES = [
          ('Manager','Manager'),
          ('teamleader','teamleader'),
          ('Employee','Employee'),
     ]
     username = None
     email = models.EmailField(unique=True,max_length=100)
     role = models.CharField(max_length=40,choices=ROLE_CHOICES)

     USERNAME_FIELD = 'email'
     REQUIRED_FIELDS = []
     objects = CustomUserManager()
     
     def __str__(self):
          return f"E-mail => {self.email}"
     
     def get_full_name(self):
          return self.first_name +" "+self.last_name