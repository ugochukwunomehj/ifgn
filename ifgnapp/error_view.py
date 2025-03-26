from django.shortcuts import render

def error_404(request, exception=None):
    return render(request, 'ifgnapp/error.html', {})

def error_403(request, exception=None):
    return render(request, 'ifgnapp/error.html', {})

def error_400(request, exception=None):
    return render(request, 'ifgnapp/error.html', {})

def error_500(request, exception=None):
    return render(request, 'ifgnapp/error.html', {})


