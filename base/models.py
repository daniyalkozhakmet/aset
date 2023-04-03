from urllib import response
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
class UserManager(BaseUserManager):
    def create_user(self, email,password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),       
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        user = self.create_user(
            email,
            password=password
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    objects = UserManager()
    first_name=models.CharField(max_length=50,blank=True,null=True)
    last_name=models.CharField(max_length=50,blank=True,null=True)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False) # a admin user; non super-user
    is_admin = models.BooleanField(default=False) # a superuser
    registered_at=models.DateField(auto_now_add=True)
    # notice the absence of a "Password field", that is built in.

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # Email & Password are required by default.

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.is_admin
class Category(models.Model):
    name=models.CharField(max_length=255,null=True,blank=True)
    def __str__(self):
        return self.name
class Sub_category(models.Model):
    name=models.CharField(max_length=255,null=True,blank=True)
    category_id=models.ForeignKey(Category,on_delete=models.CASCADE)
    def __str__(self):
        return self.name
class Neighborhood(models.Model):
    name=models.CharField(max_length=255,null=True,blank=True)
    def __str__(self):
        return self.name
class Contact(models.Model):
    email=models.CharField(max_length=255,null=True,blank=True)
    phone=models.CharField(max_length=255,null=True,blank=True)
class Complaint(models.Model):
    created_at=models.DateField(auto_now_add=True)
    is_replied=models.BooleanField(default=False)
    topic=models.TextField(null=True,blank=True)
    img=models.ImageField(null=True,blank=True,default='default.png')
    replied_at=models.DateField(auto_now_add=False,null=True,blank=True)
    description=models.TextField(null=True,blank=True)
    category_id=models.ForeignKey(Sub_category,on_delete=models.CASCADE)
    neighborhood_id=models.ForeignKey(Neighborhood,on_delete=models.CASCADE)
    users_id=models.ForeignKey(User,on_delete=models.CASCADE)
    contact_id=models.ForeignKey(Contact,on_delete=models.SET_NULL,null=True,blank=True)
    response=models.TextField(null=True,blank=True)
    def __str__(self):
        return self.topic
    