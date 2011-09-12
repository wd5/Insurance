# -*- coding: utf-8 -*-
from django.shortcuts import render

from news.models import NewsItem



def home(request, template_name="index.html"):
    items = NewsItem.objects.filter(published=True)
    context = {
        "other": items.filter(type="other")[:2],
        "news": items.filter(type="news")[:2],
        "announce": items.filter(type="announce")[:2],
    }
    return render(request, template_name, context)
    
