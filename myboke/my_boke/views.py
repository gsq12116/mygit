from django.shortcuts import render

# Create your views here.
from my_boke.models import Article


def index(request):
    if request.method == 'GET':
        articles = Article.objects.all()
        return render(request, 'index.html', {'articles': articles})


def info(request, a_id):
    if request.method == 'GET':
        article = Article.objects.filter(pk=a_id).first()
        return render(request, 'info.html', {'article': article})
