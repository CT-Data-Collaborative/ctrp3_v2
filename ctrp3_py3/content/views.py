from django.shortcuts import render
from .models import HomePage

def home_page(request):
    home_page_content = HomePage.load()
    context = {
        'about': home_page_content.about__markdownify
    }
    return render(request, 'content/home.html', context)
