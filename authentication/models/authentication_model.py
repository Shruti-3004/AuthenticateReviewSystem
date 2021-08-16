from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from authentication.manager import UserManager
from rest_framework_simplejwt.tokens import RefreshToken



class CustomUser(AbstractBaseUser):
    
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    ) 
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=False)
    staff = models.BooleanField(default=False) # a admin user; non super-user
    admin = models.BooleanField(default=False) # a superuser
    mobile_number = models.CharField(max_length=10)
    last_logout = models.DateTimeField(verbose_name='last logout', auto_now = True)
    failed_attempt = models.BooleanField(default=False)
    blocker_timer = models.DateTimeField(verbose_name='last logout', auto_now = True)
    otp_secret_token = models.CharField(max_length=100)
    otp_client_token = models.CharField(max_length=100)
    twofa_client_token = models.CharField(max_length=100)
    twofa_secret_token = models.CharField(max_length=100)
    is_email_verified = models.BooleanField(default=False)
    is_mobile_verified = models.PositiveIntegerField(default=0)
    is_otp_required = models.PositiveIntegerField(default=0)

    # notice the absence of a "Password field", that is built in.

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name'] # Email & Password are required by default.

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

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
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

    objects = UserManager()