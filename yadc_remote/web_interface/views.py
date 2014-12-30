from django.shortcuts import render, redirect
from django.http import HttpResponse

def main(request):
    return HttpResponse('hello')

def root_redirect(request):
    return redirect('web_interface.views.main')
