from django.contrib.auth.models import AbstractUser
from django.db import models

from account.managers import CustomUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from account.managers import CustomUserManager

JOB_TYPE = (
    ('M', "Male"),
    ('F', "Female"),
)

ROLE = (
    ('employer', "Employer"),
    ('employee', "Employee"),
)

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, blank=False,
                              error_messages={
                                  'unique': "Já existe um usuário com esse email.",
                              })
    role = models.CharField(choices=ROLE,  max_length=10)
    gender = models.CharField(choices=JOB_TYPE, max_length=1)
    telefone = models.CharField(max_length=20, blank=True)
    # Address fields
    
    cep = models.CharField(max_length=10, blank=True, null=True)
    rua = models.CharField(max_length=100, blank=True, null=True)    
    numero = models.CharField(max_length=10, blank=True, null=True)
    bairro = models.CharField(max_length=100, blank=True, null=True)
    cidade = models.CharField(max_length=100, blank=True, null=True)
    estado = models.CharField(max_length=100, blank=True, null=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.first_name+ ' ' + self.last_name
    objects = CustomUserManager()
