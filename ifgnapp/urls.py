from django.urls import path
from django.conf import settings
from django.urls import re_path
from django.views.static import serve

from . import views, icons
# from . import views, search_v, api


app_name = 'ifgnapp'

urlpatterns = [
    path('', views.home, name='home'),
    path('about-us/', views.about, name='about_us'),
    path('terms-privacy/', views.terms, name='terms_and_privacy'),
    path('case-studies/', views.caseStudies, name='case_studies'),
    path('courses/', views.courses, name='our_courses'),
    path('images/gallery/', views.img_gal, name='image_gallery'),
    path('contact-us/', views.contact, name='contact_us'),


    path('blog/', views.our_blog, name='our_blog'),
    path('post/<c_type>/<cnt_str>/', views.single_post, name='post'),

    path('cntfrm/', views.contact_form, name='contact_form'),


     # svg icon urls
    path('fb-icon.svg', icons.fb_ico, name='fbicon'),
    path('insta-icon.svg', icons.insta_ico, name='ig_icon'),
    path('twit-icon.svg', icons.twit_ico, name='tw_icon'),
    path('yt-icon.svg', icons.yt_ico, name='yt_icon'),
    path('web.svg', icons.globe_ico, name='web'),
    path('linked-icon.svg', icons.linkd_ico, name='linkedin_icon'),
    path('telg-icon.svg', icons.telegm_ico, name='telegram_icon'),
    path('mail-icon.svg', icons.mail_ico, name='mail_icon'),
    path('wtp-icon.svg', icons.whatsapp_ico, name='whatsapp_icon'),
    path('share-icon.svg', icons.share_ico, name='share_ico'),

]

urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]

