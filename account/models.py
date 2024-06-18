from django.contrib.auth.models import AbstractUser
from django.db import models

from account.managers import CustomUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from account.managers import CustomUserManager
from ckeditor.fields import RichTextField

JOB_TYPE = (
    ('M', "Male"),
    ('F', "Female"),
)

ROLE = (
    ('employer', "Employer"),
    ('employee', "Employee"),
    ('kenai', 'Kenai'),
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
    
    cep = models.CharField(max_length=10, blank=True, null=True, default="")
    rua = models.CharField(max_length=100, blank=True, null=True, default="")    
    numero = models.CharField(max_length=10, blank=True, null=True, default="")
    bairro = models.CharField(max_length=100, blank=True, null=True, default="")
    cidade = models.CharField(max_length=100, blank=True, null=True, default="")
    estado = models.CharField(max_length=100, blank=True, null=True, default="")

    #informacoes adicionais
    logo_empresa = models.ImageField(upload_to='logos/', blank=True, null=True, default="")
    biografia = RichTextField(blank=True, null=True, default="")
    profissao = models.CharField(max_length=255, blank=True, null=True, default="")
    especialidade = models.CharField(max_length=255, blank=True, null=True, default="")
    ferramentas = models.CharField(max_length=255, blank=True, null=True, default="")
    idiomas = models.CharField(max_length=255, blank=True, null=True, default="")
    arquivo = models.FileField(upload_to='arquivos/', blank=True, null=True, default="")
    link_video = models.CharField(max_length=255, blank=True, null=True, default="")

    #redes sociais

    facebook = models.CharField(max_length=255, null=True, blank=True, default="")
    instagram = models.CharField(max_length=255, null=True, blank=True, default="")
    linkedin = models.CharField(max_length=255, null=True, blank=True, default="")
    twitter = models.CharField(max_length=255, null=True, blank=True, default="")
    youtube = models.CharField(max_length=255, null=True, blank=True, default="")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.first_name+ ' ' + self.last_name
    objects = CustomUserManager()
