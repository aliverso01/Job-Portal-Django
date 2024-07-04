from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.http import Http404, HttpResponseRedirect, JsonResponse
from django.core.serializers import serialize
from django.views.decorators.cache import cache_page
from django.core.cache import cache
import requests
from django.conf import settings
from .utils import get_efipay_token, create_split_payment

from account.models import User
from jobapp.forms import *
from jobapp.models import *
from jobapp.permission import *
User = get_user_model()


def home_view(request):

    published_jobs = Job.objects.filter(is_published=True).order_by('-timestamp')
    jobs = published_jobs.filter(is_closed=False)
    total_candidates = User.objects.filter(role='employee').count()
    total_companies = User.objects.filter(role='employer').count()
    paginator = Paginator(jobs, 3)
    page_number = request.GET.get('page',None)
    page_obj = paginator.get_page(page_number)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        job_lists=[]
        job_objects_list = page_obj.object_list.values()
        for job_list in job_objects_list:
            job_lists.append(job_list)
        

        next_page_number = None
        if page_obj.has_next():
            next_page_number = page_obj.next_page_number()

        prev_page_number = None       
        if page_obj.has_previous():
            prev_page_number = page_obj.previous_page_number()

        data={
            'job_lists':job_lists,
            'current_page_no':page_obj.number,
            'next_page_number':next_page_number,
            'no_of_page':paginator.num_pages,
            'prev_page_number':prev_page_number
        }    
        return JsonResponse(data)
    
    context = {

    'total_candidates': total_candidates,
    'total_companies': total_companies,
    'total_jobs': len(jobs),
    'total_completed_jobs':len(published_jobs.filter(is_closed=True)),
    'page_obj': page_obj
    }
    print('ok')
    return render(request, 'jobapp/index.html', context)

@cache_page(60 * 15)
def job_list_View(request):
    """

    """
    job_list = Job.objects.filter(is_published=True,is_closed=False).order_by('-timestamp')
    paginator = Paginator(job_list, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {

        'page_obj': page_obj,

    }
    return render(request, 'jobapp/job-list.html', context)



@login_required(login_url=reverse_lazy('account:login'))
@user_is_employer
def create_job_View(request):
    """
    Provide the ability to create job post
    """
    form = JobForm(request.POST or None)
    user = get_object_or_404(User, id=request.user.id)

    if request.method == 'POST':
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = user
            instance.save()

            # Criando automaticamente uma aprovação para este job
            Aprovacao.objects.create(job=instance, user=request.user)

            messages.success(
                request, 'Você publicou seu trabalho com sucesso! Por favor, aguarde a revisão.')
            return redirect(reverse("jobapp:single-job", kwargs={'id': instance.id}))

    context = {
        'form': form,
    }
    return render(request, 'jobapp/post-job.html', context)


@login_required(login_url=reverse_lazy('account:login'))
def single_job_view(request, id):
    job = get_object_or_404(Job, id=id)

    # Busca a primeira aprovação para o job
    aprovacao = Aprovacao.objects.filter(job=job).first()

    # Não é necessário armazenar no cache novamente se já foi obtido com get_object_or_404
    # if cache.get(id):
    #     job = cache.get(id)
    # else:
    #     job = get_object_or_404(Job, id=id)
    #     cache.set(id, job, 60 * 15)

    related_job_list = job.tags.similar_objects()

    paginator = Paginator(related_job_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    form = JobForm(request.POST or None)

    # Verificação de formulário não é necessária para a funcionalidade principal
    # if form.is_valid():
    #     instance = form.save(commit=False)
    #     instance.save()
    #     messages.success(request, 'Your Comment Was Successfully Posted!')
    #     return HttpResponseRedirect(reverse("jobapp:single-job", kwargs={'id': id}))

    context = {
        'job': job,
        'page_obj': page_obj,  # Passa page_obj para o template
        'total': len(related_job_list),
        'form': form,
        'aprovacao': aprovacao,
    }

    return render(request, 'jobapp/job-single.html', context)



def search_result_view(request):
    """
        User can search job with multiple fields

    """

    job_list = Job.objects.order_by('-timestamp')

    # Keywords
    if 'job_title_or_company_name' in request.GET:
        job_title_or_company_name = request.GET['job_title_or_company_name']

        if job_title_or_company_name:
            job_list = job_list.filter(title__icontains=job_title_or_company_name) | job_list.filter(
                company_name__icontains=job_title_or_company_name)

    # location
    if 'location' in request.GET:
        location = request.GET['location']
        if location:
            job_list = job_list.filter(location__icontains=location)

    # Job Type
    if 'job_type' in request.GET:
        job_type = request.GET['job_type']
        if job_type:
            job_list = job_list.filter(job_type__iexact=job_type)

    # job_title_or_company_name = request.GET.get('text')
    # location = request.GET.get('location')
    # job_type = request.GET.get('type')

    #     job_list = Job.objects.all()
    #     job_list = job_list.filter(
    #         Q(job_type__iexact=job_type) |
    #         Q(title__icontains=job_title_or_company_name) |
    #         Q(location__icontains=location)
    #     ).distinct()

    # job_list = Job.objects.filter(job_type__iexact=job_type) | Job.objects.filter(
    #     location__icontains=location) | Job.objects.filter(title__icontains=text) | Job.objects.filter(company_name__icontains=text)

    paginator = Paginator(job_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {

        'page_obj': page_obj,

    }
    return render(request, 'jobapp/result.html', context)


@login_required(login_url=reverse_lazy('account:login'))
@user_is_employee
def apply_job_view(request, id):

    form = JobApplyForm(request.POST or None)

    user = get_object_or_404(User, id=request.user.id)
    applicant = Applicant.objects.filter(user=user, job=id)
    job = get_object_or_404(Job, id=id)
    
    if not applicant:
        if request.method == 'POST':

            if form.is_valid():
                instance = form.save(commit=False)
                instance.user = user
                instance.status = '2'
                instance.save()

                job.status = '2'
                job.save()

                messages.success(
                    request, 'You have successfully applied for this job!')
                return redirect(reverse("jobapp:single-job", kwargs={
                    'id': id
                }))

        else:
            return redirect(reverse("jobapp:single-job", kwargs={
                'id': id
            }))

    else:

        messages.error(request, 'You already applied for the Job!')

        return redirect(reverse("jobapp:single-job", kwargs={
            'id': id
        }))


@login_required(login_url=reverse_lazy('account:login'))
def dashboard_view(request):
    """
    """
    jobs = []
    savedjobs = []
    appliedjobs = []
    total_applicants = {}
    if request.user.role == 'employer':

        jobs = Job.objects.filter(user=request.user.id)
        for job in jobs:
            count = Applicant.objects.filter(job=job.id).count()
            total_applicants[job.id] = count

    if request.user.role == 'employee':
        savedjobs = BookmarkJob.objects.filter(user=request.user.id)
        appliedjobs = Applicant.objects.filter(user=request.user.id)
    context = {

        'jobs': jobs,
        'savedjobs': savedjobs,
        'appliedjobs':appliedjobs,
        'total_applicants': total_applicants
    }

    return render(request, 'jobapp/dashboard.html', context)


@login_required(login_url=reverse_lazy('account:login'))
@user_is_employer
def delete_job_view(request, id):

    job = get_object_or_404(Job, id=id, user=request.user.id)

    if job:

        job.delete()
        messages.success(request, 'Your Job Post was successfully deleted!')

    return redirect('jobapp:dashboard')


@login_required(login_url=reverse_lazy('account:login'))
@user_is_employer
def make_complete_job_view(request, id):
    job = get_object_or_404(Job, id=id, user=request.user.id)

    if job:
        try:
            job.is_closed = True
            job.save()
            messages.success(request, 'Your Job was marked closed!')
        except:
            messages.success(request, 'Something went wrong !')
            
    return redirect('jobapp:dashboard')



@login_required(login_url=reverse_lazy('account:login'))
@user_is_employer
def all_applicants_view(request, id):

    all_applicants = Applicant.objects.filter(job=id)

    context = {

        'all_applicants': all_applicants
    }

    return render(request, 'jobapp/all-applicants.html', context)


@login_required(login_url=reverse_lazy('account:login'))
@user_is_employee
def delete_bookmark_view(request, id):

    job = get_object_or_404(BookmarkJob, id=id, user=request.user.id)

    if job:

        job.delete()
        messages.success(request, 'Saved Job was successfully deleted!')

    return redirect('jobapp:dashboard')


@login_required(login_url=reverse_lazy('account:login'))
@user_is_employer
def applicant_details_view(request, id):

    applicant = get_object_or_404(User, id=id)

    context = {

        'applicant': applicant
    }

    return render(request, 'jobapp/applicant-details.html', context)


@login_required(login_url=reverse_lazy('account:login'))
@user_is_employee
def job_bookmark_view(request, id):

    form = JobBookmarkForm(request.POST or None)

    user = get_object_or_404(User, id=request.user.id)
    applicant = BookmarkJob.objects.filter(user=request.user.id, job=id)
    job = get_object_or_404(Job, id=id)

    if not applicant:
        if request.method == 'POST':

            if form.is_valid():
                instance = form.save(commit=False)
                instance.user = user
                instance.status = '3'
                instance.save()

                job.status = '3'
                job.save()

                messages.success(
                    request, 'You have successfully save this job!')
                return redirect(reverse("jobapp:single-job", kwargs={
                    'id': id
                }))

        else:
            return redirect(reverse("jobapp:single-job", kwargs={
                'id': id
            }))

    else:
        messages.error(request, 'Você enviou para aprovação!')

        return redirect(reverse("jobapp:single-job", kwargs={
            'id': id
        }))

@login_required(login_url=reverse_lazy('account:login'))
@user_is_employer
def aprovar_job_view(request, id):
    job = get_object_or_404(Job, id=id, user=request.user.id)

    form = JobEditForm(request.POST or None, instance=job)

    if form.is_valid():
        instance = form.save(commit=False)
        instance.status = '4'
        instance.save()

        job.status = '4'
        job.save()
        messages.success(request, 'Enviado para aprovação')

    return redirect('jobapp:dashboard')

@login_required(login_url=reverse_lazy('account:login'))
@user_is_employer
def job_aprovado_view(request, id):
    job = get_object_or_404(Job, id=id, user=request.user.id)

    # Atualiza o status do job para '5' diretamente
    job.status = '5'
    job.save()

    # Redireciona para a página de pagamento
    return redirect('jobapp:pagamento', job_id=job.id)

@login_required(login_url=reverse_lazy('account:login'))
@user_is_employee
def aprovar_material_view(request, id):
    job = get_object_or_404(Job, id=id, user=request.user.id)

    form = JobEditForm(request.POST or None, instance=job)

    if job:
        if form.is_valid():
            instance = form.save(commit=False)
            instance.status = '4'
            instance.save()
            messages.success(request, 'Aprovado com sucesso!')
        else:
            messages.success(request, 'Algo deu errado!')

    context = {
        'form': form,
    }

    return redirect('jobapp:dashboard',)



@login_required(login_url=reverse_lazy('account:login'))
@user_is_employer
def job_edit_view(request, id=id):
    """
    Handle Job Update

    """

    job = get_object_or_404(Job, id=id, user=request.user.id)
    # categories = Category.objects.all()
    form = JobEditForm(request.POST or None, instance=job)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        # for save tags
        # form.save_m2m()
        messages.success(request, 'Your Job Post Was Successfully Updated!')
        return redirect(reverse("jobapp:single-job", kwargs={
            'id': instance.id
        }))
    context = {

        'form': form,
        # 'categories': categories
    }

    return render(request, 'jobapp/job-edit.html', context)





#personalizados




@login_required(login_url=reverse_lazy('account:login'))
@user_is_employee
def envia_material_view(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    aprovacoes = Aprovacao.objects.filter(job=job, user=request.user)

    if aprovacoes.exists():  # Verifica se há pelo menos uma aprovação
        aprovacao = aprovacoes.first()  # Pega a primeira aprovação encontrada
    else:
        aprovacao = None

    if request.method == 'POST':
        form = EnviaMaterialForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.job = job
            instance.user = request.user
            instance.status = '3'
            instance.save()

            job.status = '3'
            job.save()

            messages.success(request, 'Material enviado com sucesso!')
            return redirect('jobapp:dashboard')
    else:
        form = EnviaMaterialForm()

    context = {
        'form': form,
        'job': job,
        'aprovacao': aprovacao,
    }
    return render(request, 'jobapp/envia-material.html', context)

@login_required(login_url=reverse_lazy('account:login'))
@user_is_employee
def envia_material_edit_view(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    aprovacoes = Aprovacao.objects.filter(job=job, user=request.user)

    if aprovacoes.exists():  # Verifica se há pelo menos uma aprovação
        aprovacao = aprovacoes.first()  # Pega a primeira aprovação encontrada
    else:
        raise Http404("Aprovação não encontrada para este usuário e job.")

    if request.method == 'POST':
        form = EnviaMaterialForm(request.POST, request.FILES, instance=aprovacao)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.job = job
            instance.user = request.user
            instance.status = '3'
            instance.save()

            job.status = '3'
            job.save()

            messages.success(request, 'Material atualizado com sucesso!')
            return redirect('jobapp:dashboard')
    else:
        form = EnviaMaterialForm(instance=aprovacao)

    context = {
        'form': form,
        'job': job,
        'aprovacao': aprovacao,
    }
    return render(request, 'jobapp/envia-material.html', context)


#pagina de checkout

@login_required(login_url=reverse_lazy('account:login'))
@user_is_employer
def pagina_pagamento_view(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    pix_qr_code = None  # Placeholder para o QR code Pix

    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            amount = int(job.salary * 100)  # Convertendo o valor para centavos
            recipient_list = [
                {
                    "chave": "chave_pix_recebedor_1",
                    "valor": int(amount * 0.5)  # Exemplo: 50% do valor total
                },
                {
                    "chave": "chave_pix_recebedor_2",
                    "valor": int(amount * 0.5)  # Exemplo: 50% do valor total
                }
            ]

            payment_response = create_split_payment(amount, recipient_list)
            
            if 'erro' in payment_response:
                # Lidar com erro
                context = {
                    'job': job,
                    'form': form,
                    'error': payment_response['erro']
                }
                return render(request, 'billing/billing.html', context)

            # Gerar QR code Pix e redirecionar para a página de confirmação ou sucesso
            pix_qr_code = payment_response.get('qr_code_url')
            return redirect(reverse('jobapp:pagina_de_sucesso'))

    else:
        form = JobForm()

    context = {
        'job': job,
        'form': form,
        'pix_qr_code': pix_qr_code,
    }

    return render(request, 'billing/billing.html', context)

def pagina_sucesso_view(request):
    return render(request, 'billing/success.html')



def alteracao_view(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    if request.method == 'POST':
        form = AlteracaoForm(request.POST, instance=job)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.status = '4'  # Atualiza o status para 4
            instance.save()
            return redirect('jobapp:dashboard')  # Redireciona para a dashboard após a atualização
    else:
        form = AlteracaoForm(instance=job)

    context = {
        'form': form,
        'job': job,
    }

    return render(request, 'jobapp/alteracao.html', context)