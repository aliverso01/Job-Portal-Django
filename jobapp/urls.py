from django.urls import path
from jobapp import views

app_name = "jobapp"


urlpatterns = [

    path('', views.home_view, name='home'),
    path('jobs/', views.job_list_View, name='job-list'),
    path('job/create/', views.create_job_View, name='create-job'),
    path('job/aprov/<int:id>/', views.aprovar_job_view, name='aprov-job'),
    path('job/aprovado/<int:id>/', views.job_aprovado_view, name='job-aprovado'),
    path('job/aprovar/material/<int:id>/', views.aprovar_material_view, name='aprov-material'),
    path('job/<int:id>/', views.single_job_view, name='single-job'),
    path('apply-job/<int:id>/', views.apply_job_view, name='apply-job'),
    path('bookmark-job/<int:id>/', views.job_bookmark_view, name='bookmark-job'),
    path('about/', views.single_job_view, name='about'),
    path('contact/', views.single_job_view, name='contact'),
    path('result/', views.search_result_view, name='search_result'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('dashboard/employer/job/<int:id>/applicants/', views.all_applicants_view, name='applicants'),
    path('dashboard/employer/job/edit/<int:id>', views.job_edit_view, name='edit-job'),
    path('dashboard/employer/applicant/<int:id>/', views.applicant_details_view, name='applicant-details'),
    path('dashboard/employer/close/<int:id>/', views.make_complete_job_view, name='complete'),
    path('dashboard/employer/delete/<int:id>/', views.delete_job_view, name='delete'),
    path('dashboard/employee/delete-bookmark/<int:id>/', views.delete_bookmark_view, name='delete-bookmark'),
    #personalizados
    path('envia-material/<int:job_id>/', views.envia_material_view, name='envia-material'),
    path('envia-material-edit/<int:job_id>/', views.envia_material_edit_view, name='envia-material-edit'),
    path('alteracao/<int:job_id>/', views.alteracao_view, name='alteracao'),

    #pagamento
    path('billing/<int:job_id>/', views.pagina_pagamento_view, name='pagamento'),
    path('pagamento/sucesso/', views.pagina_sucesso_view, name='pagina_de_sucesso'),
]

