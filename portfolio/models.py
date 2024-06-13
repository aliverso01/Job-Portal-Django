from django.db import models
from ckeditor.fields import RichTextField
from account.models import User
# Create your models here.

class Portfolio(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    logo_empresa = models.ImageField(upload_to='logos/')
    biografia = RichTextField()
    profissao = models.CharField(max_length=255)
    especialidade = models.CharField(max_length=255)
    ferramentas = models.CharField(max_length=255)
    idiomas = models.CharField(max_length=255)
    arquivo = models.FileField(upload_to='arquivos/')
    link_video = models.CharField(max_length=255)

    #redes sociais

    facebook = models.CharField(max_length=255)
    instagram = models.CharField(max_length=255)
    linkedin = models.CharField(max_length=255)
    twitter = models.CharField(max_length=255)
    youtube = models.CharField(max_length=255)

    #estilização
    background_color = models.CharField(max_length=255)
    button_color = models.CharField(max_length=255)
    text_color = models.CharField(max_length=255)
    font_size = models.CharField(max_length=255)
    font_family = models.CharField(max_length=255)
    border_radius = models.CharField(max_length=255)