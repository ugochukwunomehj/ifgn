
from django.shortcuts import render
from. import models

def robot_file(request):
    return render(request, 'ifgnapp/seofiles/robot.txt', {}, content_type='text/plain')

def manifest_file(request):
    return render(request, 'ifgnapp/seofiles/manifest.json', {}, content_type='application/json')

def open_search(request):
    return render(request, 'ifgnapp/seofiles/searchlink.xml', {}, content_type='text/xml, application/xml')

def post_sitemap(request):
    posts = models.post.objects.all().filter(is_published=True).order_by('pub_date')
    
    res = {
        'posts': posts,
    }
    return render(request, 'ifgnapp/seofiles/post-sitemap.xml', res, content_type='text/xml, application/xml')

def sitemap(request):
    posts = models.post.objects.all().filter(is_published=True).order_by('-pub_date')
    
    res = {
        'posts': posts,
    }
    return render(request, 'ifgnapp/seofiles/sitemap.xml', res, content_type='text/xml, application/xml')

def feed(request):
    posts = models.post.objects.all().filter(is_published=True).order_by('-pub_date')[:50]
    res = {
        'posts': posts,
    }
    return render(request, 'ifgnapp/seofiles/rss.xml', res, content_type='application/rss+xml;qs=0.8')
