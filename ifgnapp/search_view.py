from django.shortcuts import render
from django.http import HttpResponse 
from django.db.models import F, Q, Max
import  re
from . import models, my_functions

def search(request):
    if request.method == "GET":
        srch_str = request.GET["s"]
        _new_str = my_functions.text_filter(my_functions.rem_words(srch_str, _len=2))
        more = models.post.objects.filter(is_published=True).order_by('-pub_date')
        trend = models.post.objects.annotate(high=Max('visit')).filter(is_published=True).order_by('?')[:10]
        viral = models.post.objects.filter(post_type__iexact="Viral").filter(is_published=True).order_by('-pub_date')[:10]
        news = models.post.objects.filter(post_type__iexact="News").filter(is_published=True).order_by('-pub_date')[:10]
        destin = models.post.objects.filter(post_type__iexact="Destinations").filter(is_published=True).order_by('-pub_date')[:10]
     
        
        # split our input so it will search per word against all the sentence..
        search_str_new = re.findall(r'(?P<x>\w+)', _new_str, re.I)
        set_ret_txt = set(search_str_new)
        set_ret_txt.discard('')

        # iterations my_functions for our models.. 
        _cont_res = []
        for _dt in set_ret_txt:
            _content_mod = models.post.objects.filter(title__icontains=_dt).filter(is_published=True)

            my_functions.loop_model(_content_mod, _cont_res)

        last_article_list = list(set(_cont_res))

        context = {
                'status': "success",
                'str': srch_str,  
                'res': last_article_list,  
                'single_all': 'yes' if len(last_article_list)<=1 else 'no',
                'more': more, 
                "trending": trend,
                "viral": viral,
                "news": news,      
                "destination": destin,      
        }  
        return(render(request, 'ifgnapp/search.html', context=context))
              