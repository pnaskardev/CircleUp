import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.utils import timezone


class CustomUserManager(UserManager):
    
    # The custom user manager is a class that inherits from the UserManager class.
    # Normally It overrides the create_user and create_superuser methods to create a user with the email as the username.
    # here we are adding name field to the create_user and create_superuser methods.
    # by overriding the create_user and create_superuser methods, we can add extra fields to the user model.
    # The ** prefix before the variable name indicates that the argument should be treated as a dictionary of key-value pairs.
    # The **extra_fields argument is used to pass a variable number of arguments to a function.
    def _create_user(self, name, email, password, **extra_fields):
        if not email:
            raise ValueError('A valid email was not provided')

        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, name=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(name, email, password, **extra_fields)

    def create_superuser(self,name=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(name, email, password, **extra_fields)
    

class User(AbstractBaseUser ,PermissionsMixin):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email=models.EmailField(unique=True)
    name=models.CharField(max_length=255, blank=True,default='')
    avatar=models.ImageField(upload_to='avatars',blank=True,null=True)
    friends = models.ManyToManyField('self')
    friends_count=models.IntegerField(default=0)

    is_active=models.BooleanField(default=True)
    is_superuser=models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)

    date_joined=models.DateTimeField(default=timezone.now)
    last_login=models.DateTimeField(blank=True,null=True)

    objects=CustomUserManager()

    USERNAME_FIELD='email'
    EMAIL_FIELD='email'
    REQUIRED_FIELDS=[]

class FriendshipRequest(models.Model):
    SENT='sent'
    ACCEPTED='accepted'
    REJECTED='rejected'

    STATUS_CHOICES=(
        (SENT,'Sent'),
        (ACCEPTED,'Accepted'),
        (REJECTED,'Rejected')
    )   

    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_for=models.ForeignKey(User,related_name='received_friendship_requests',on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    created_by=models.ForeignKey(User,related_name='created_friendship_requests',on_delete=models.CASCADE)
    status=models.CharField(max_length=20,choices=STATUS_CHOICES,default=SENT)