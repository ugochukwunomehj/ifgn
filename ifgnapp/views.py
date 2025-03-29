from django.shortcuts import render, redirect
from . import models, my_functions
from django.db.models import F, Q
from django.core.paginator import Paginator
import re, random
from django.utils.text import slugify
from django.db.models import Max
from django.http import HttpResponse, HttpResponseRedirect, FileResponse, JsonResponse
from django.urls import reverse
from django.contrib.sessions.backends.db import SessionStore
from django.views.decorators.http import require_GET as re_ge
from time import timezone
import json

@re_ge
def home(request):
    # hpg = models.site_page.objects.filter(name__iexact='home').first()
    # post = models.post.objects.order_by('-pub_date').filter(is_published=True)[:3]
    # img_gal = models.g_image.objects.order_by('-date')[:10]
    # facility = models.course.objects.order_by('?')[:4]
 
    context = {
                'status': "success",
                #  'hpg': hpg,
                #  'img_gal': img_gal,
                #  "post": post,
                #  'facility': facility,
                 }
    
    return(render(request, 'ifgnapp/home.html', context))


@re_ge
def contact(request):
    
    context = {
                'status': "success",
                'ptype': "stmcnt",
                 }
    return(render(request, 'ifgnapp/contact.html', context))


@re_ge
def courses(request):
    facility = models.course.objects.order_by('?')
    context = {
                'status': "success",
                'facility': facility,
                 }
    return(render(request, 'ifgnapp/courses.html', context))

@re_ge
def terms(request):
    
    context = {
                'status': "success",
                 }
    return(render(request, 'ifgnapp/terms.html', context))

@re_ge
def about(request):
    
    context = {
                'status': "success",
                 }
    return(render(request, 'ifgnapp/about.html', context))


@re_ge
def caseStudies(request):
    
    context = {
                'status': "success",
                 }
    return(render(request, 'ifgnapp/casestudy.html', context))


@re_ge
def our_blog(request):
     posts = models.post.objects.all().filter(is_published=True)
     
     paginator = Paginator(posts, 20)

     page_number = request.GET.get('page')
     page_obj = paginator.get_page(page_number)
    
     return render(request, 'ifgnapp/blog.html', {
          'status': "success",
          'post': page_obj,
        
          })


@re_ge
def img_gal(request):
    img_gal = models.g_image.objects.order_by('-date')
    
    context = {
                'status': "success",
                'img_gal': img_gal,
                 }
    return(render(request, 'ifgnapp/images.html', context))



@re_ge
def members(request):
    img_gal = models.g_image.objects.order_by('-date')
    
    context = {
                'status': "success",
                'img_gal': img_gal,
                 }
    return(render(request, 'ifgnapp/members.html', context))



def single_post(request, cnt_str, c_type):
    try:
        posts = models.post.objects.filter(is_published=True).filter(Q(slug_name__iexact=cnt_str) & Q(post_type__iexact=c_type)).first()
        posts_categ = posts.post_type
        more_posts = models.post.objects.filter(category__iexact=posts_categ).filter(is_published=True).order_by('-pub_date').exclude(slug_name=cnt_str)[:6]
        more = more_posts if more_posts else models.post.objects.order_by('-pub_date').filter(is_published=True).exclude(slug_name=cnt_str)[:6] 
          
        if posts.is_published == True:
            res = {
            'status': "success",
            'postsid': posts.id,
            's_title': posts.s_title,
            'slug': posts.slug_name,
            'name': posts.name,
            'title': posts.title,
            'r_time': posts.read_time,
            'des': posts.meta,
            'categ': posts.category,
            'type': posts.post_type,
            "posts": more,
            "rel": more_posts,
            'author': posts.autor,
            'content2': posts.content2,
            'g_img': posts.graph_img,
            'content3': posts.content3,
            'fcr1': posts.photo_cred1,
            'frame': posts.frame,
            'image1': posts.image1,
            'image2': posts.image2,
            'content3': posts.content3,
            'content1': posts.content1,
            'date': posts.pub_date,
        }
            if posts:
                models.post.objects.filter(slug_name=cnt_str).update(visit=F('visit') + 1) 
                posts.refresh_from_db()
            return(render(request, 'ifgnapp/single-blog.html', context=res))
        else:
            return(render(request, 'ifgnapp/single-blog.html', context={'error': 'failed', "posts": more, "more": more_posts, 
             })) 
    except:
        return(render(request, 'ifgnapp/single-blog.html', context={'error': 'failed'}))     



# contact us..
def contact_form(request):
    ip_getter = 'hide'
    try:
        x_forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded:
            ip_getter = x_forwarded.split(',')[0]
        else:
            ip_getter = request.META.get('REMOTE_ADDR')
    except:
        pass

    if request.method == 'POST':
        my_data = request.body
        _new_data  = json.loads(my_data)
        _new_email = my_functions.email_checker(_new_data.get("email"))
        _type = _new_data.get("reqtype")
        _country = _new_data.get('country')

        if _new_email == 'Invalid':
            return(JsonResponse({'W':'Invalid Email address!'}, safe=False))
        else:
            pass


        _name = _new_data.get("name")
        _msg = _new_data.get("msg")
        if _type == 'stmcnt':
            _msg = _new_data.get("msg")
            _name = _new_data.get("name")
            models.contact_us.objects.create(name=_name, email=_new_email, country=_country, user_ip=ip_getter, msg=_msg)
            return(JsonResponse({'S':'Thanks, for sending us a message!'}, safe=False)) 
        else:
            return(JsonResponse({'W':'Invalid input please try again!'}, safe=False))
        
        # print(f'\n----------------\n You made a request here! \n------------------\n')
        # return(JsonResponse({'S':'Thanks, for sending us a message!'}, safe=False)) 
    else:
        return(JsonResponse({'E':'Sorry, an error occurred!'}, safe=False))   

