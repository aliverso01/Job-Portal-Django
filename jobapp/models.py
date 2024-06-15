from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
User = get_user_model()


from ckeditor.fields import RichTextField
from taggit.managers import TaggableManager


JOB_TYPE = (
    ('1', "Edição de vídeo"),
    ('2', "Captação de imagem"),
    ('3', "Design Gráfico"),
    ('4', "Web Design"),
    ('5', "Animação 2d/3d"),
    ('6', "Motion Designer"),
    ('7', "Produtor"),
    ('8', "Roteirista"),
    ('9', "Social Média"),
)

PROPORCAO = (
    ('1', "horizontal"),
    ('2', "quadrado"),
    ('3', "vertical"),
    ('4', "outro")
)

STATUS = (
    ('1', "Buscando Profissional"),
    ('2', "Em andamento"),
    ('3', "Aprovação do Cliente"),
    ('4', "Solicitado Alteração"),
    ('5', "Aguardando Pagamento"),
    ('6', "Finalizado"),
    ('7', "Cancelado"),
)
    

# class Category(models.Model):
#     name = models.CharField(max_length=50)

#     def __str__(self):
#         return self.name
    

class Job(models.Model):

    user = models.ForeignKey(User, related_name='User', on_delete=models.CASCADE) 
    title = models.CharField(max_length=300)
    description = RichTextField()
    tags = TaggableManager()
    location = models.CharField(max_length=300)
    job_type = models.CharField(choices=JOB_TYPE, max_length=1)
    # category = models.ForeignKey(Category,related_name='Category', on_delete=models.CASCADE)
    salary = models.CharField(max_length=30, blank=True)
    # company_name = models.CharField(max_length=300)
    # company_description = RichTextField(blank=True, null=True)
    url = models.URLField(max_length=200)
    last_date = models.DateField()
    is_published = models.BooleanField(default=False)
    is_closed = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now=True)

    #campos personalizados
    proporcional = models.CharField(choices=PROPORCAO, max_length=1)
    tempo_video = models.CharField(max_length=30, blank=True)

    status = models.CharField(choices=STATUS, max_length=1, default='1')


    def __str__(self):
        return self.title

 

class Applicant(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True, auto_now_add=False)


    def __str__(self):
        return self.job.title


  

class BookmarkJob(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True, auto_now_add=False)


    def __str__(self):
        return self.job.title