from django.urls import path
from portfolio import views

app_name = "portfolio"

urlpatterns = [
    path('portfolio/', views.portfolio, name='portfolio'),
    path('portfolio/edit/<int:id>/', views.edit_portfolio, name='edit-portfolio'),
    path('portfolio/delete/<int:id>/', views.delete_portfolio, name='delete-portfolio'),
    path('portfolio/add/', views.add_portfolio, name='add-portfolio'),
]