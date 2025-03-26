from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from. import models
# import pyttsx3


def yt_ico(requset):
    return(render(requset, 'ifgnapp/icons/ytb-icon.svg', {}, content_type='image/svg+xml,'))

def fb_ico(requset):
    return(render(requset, 'ifgnapp/icons/fb-icon.svg', {}, content_type='image/svg+xml,'))

def linkd_ico(requset):
    return(render(requset, 'ifgnapp/icons/linkd-icon.svg', {}, content_type='image/svg+xml,'))

def telegm_ico(requset):
    return(render(requset, 'ifgnapp/icons/teleg-icon.svg', {}, content_type='image/svg+xml,'))

def whatsapp_ico(requset):
    return(render(requset, 'ifgnapp/icons/whatsapp-icon.svg', {}, content_type='image/svg+xml,'))

def mail_ico(requset):
    return(render(requset, 'ifgnapp/icons/mail-icon.svg', {}, content_type='image/svg+xml,'))

def globe_ico(requset):
    return(render(requset, 'ifgnapp/icons/globe.svg', {}, content_type='image/svg+xml,'))

def insta_ico(requset):
    return(render(requset, 'ifgnapp/icons/insta-icon.svg', {}, content_type='image/svg+xml,'))

def twit_ico(requset):
    return(render(requset, 'ifgnapp/icons/twit-icon.svg', {}, content_type='image/svg+xml,'))

def share_ico(requset):
    return(render(requset, 'ifgnapp/icons/share-icon.svg', {}, content_type='image/svg+xml,'))