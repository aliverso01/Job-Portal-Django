from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from portfolio.models import Portfolio

@login_required
def portfolio(request):
    user = request.user  # Já temos o usuário logado diretamente do request
    portfolio = Portfolio.objects.filter(user=user)
    
    context = {
        'portfolio': portfolio,
    }

    return render(request, 'portfolio/portfolio.html', context)

@login_required
def edit_portfolio(request, id):
    portfolio = Portfolio.objects.get(id=id)
    context = {
        'portfolio': portfolio,
    }

    return render(request, 'portfolio/edit_portfolio.html', context)

@login_required
def delete_portfolio(request, id):
    portfolio = Portfolio.objects.get(id=id)
    portfolio.delete()
    return redirect('portfolio:portfolio')

@login_required
def add_portfolio(request):
    return render(request, 'portfolio/add_portfolio.html')
