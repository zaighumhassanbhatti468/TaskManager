from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, fullname, phonenumber, email, password=None, role=None, address=""):
        if not fullname:
            raise ValueError("Full name is required")
        if not phonenumber:
            raise ValueError("Phone number is required")
        if not email:
            raise ValueError("Email is required")
        if not password:
            raise ValueError("Password is required")

        user = self.model(
            fullname=fullname,
            phonenumber=phonenumber,
            email=self.normalize_email(email),
            role=role,
            address=address
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, fullname, phonenumber, email, password):
        user = self.create_user(fullname, phonenumber, email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    fullname = models.CharField(max_length=255)
    phonenumber = models.CharField(max_length=15, unique=True)
    address = models.TextField(blank=True, null=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    role = models.ForeignKey('Role', on_delete=models.SET_NULL, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["fullname", "phonenumber", "password"]

    def __str__(self):
        return self.fullname
