# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.shortcuts import get_object_or_404

from news.models import NewsItem



def news_item(request, item_id, template_name='news/news_item.html'):
    item = get_object_or_404(NewsItem, pk=item_id)
    return render(request, template_name, {"news_item": item})
    
