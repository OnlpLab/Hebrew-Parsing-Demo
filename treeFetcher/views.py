from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from .forms import UtteranceForm, ConllForm, ContactForm
from .conll_file_fetcher import parse_sentence, morphological_analyzer, show_dependencies, segment_query, pos_tagger
from .models import DepCategory
from django.core.mail import send_mail, BadHeaderError
from django.template import RequestContext
from django.contrib import messages
import subprocess
# Create your views here.
import time


def home(request):
    return render(request, 'index.html')

def landing_page(request):
    sent = False
    if request.method == 'GET':
        contact = ContactForm()
    else:
        contact = ContactForm(request.POST)
        if contact.is_valid():
            subject = contact.cleaned_data.get('subject')
            from_email = contact.cleaned_data.get('contact_email')
            message = contact.cleaned_data.get('message')
            name = contact.cleaned_data.get('contact_name')
            everything = "Name: %s\n\nSubject: %s\n\nEmail: %s \n\nMessage: %s \n\n"%(str(name), str(subject), str(from_email), str(message))
            try:
                send_mail(subject, everything, from_email, ['onlp.biu@gmail.com'])#, 'reut.tsarfaty@biu.ac.il'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            sent = True
            messages.success(request, 'Your message was successfully sent. Thank you!')
            return redirect('https://nlp.biu.ac.il/~rtsarfaty/onlp#contact')
    return render(request, "home.html", {'contact': contact, 'sent': sent})

def about(request):
    return render(request, 'about.html')


def postags(request):
    return render(request, 'postags.html')


def spmrl_dependencies(request):
    return render(request, 'spmrl_dependencies.html')

def spmrl_features(request):
    return render(request, 'spmrl_features.html')


def documentation(request):
    # relations = DepCategory.objects.all()
    return render(request, "documentation.html")

def resources(request):
    # relations = DepCategory.objects.all()
    return render(request, "resources.html")

def faq(request):
    # relations = DepCategory.objects.all()
    return render(request, "faq.html")


def contact(request):
    sent = False
    if request.method == 'GET':
        contact = ContactForm()
    else:
        contact = ContactForm(request.POST)
        if contact.is_valid():
            subject = contact.cleaned_data.get('subject')
            from_email = contact.cleaned_data.get('contact_email')
            message = contact.cleaned_data.get('message')
            name = contact.cleaned_data.get('contact_name')
            everything = "Name: %s\n\nSubject: %s\n\nEmail: %s \n\nMessage: %s \n\n"%(str(name), str(subject), str(from_email), str(message))
            try:
                send_mail(subject, everything, from_email, ['onlp.biu@gmail.com'])#, 'reut.tsarfaty@biu.ac.il'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            sent = True
            messages.success(request, 'Your message was successfully sent. Thank you!')
            return redirect('https://nlp.biu.ac.il/~rtsarfaty/onlp/hebrew/contact')
    return render(request, "contact.html", {'contact': contact, 'sent': sent})



def handler404(request):
    response = render('404.html', {}, context_instance=RequestContext(request))
    response.status_code = 404
    return response