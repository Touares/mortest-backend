from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    # user_type_data = (('1',"Directeur"),('2',"Vendeur"),('3',"Autre"))
    # user_type = models.CharField(default='2',choices=user_type_data,max_length=10)
    REQUIRED_FIELDS = []
    objects = CustomUserManager()
    # date_of_birth = models.DateField(blank=True, null=True)
    
    def __str__(self) -> str:
        return f'{self.username}'
