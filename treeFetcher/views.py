from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from .forms import UtteranceForm, ConllForm, ContactForm, ReportForm
from .conll_file_fetcher import parse_sentence, morphological_analyzer, show_dependencies, segment_query, pos_tagger
from .models import DepCategory
from django.core.mail import send_mail, BadHeaderError
from django.template import RequestContext
import subprocess
# Create your views here.
import time


def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def submit_utterance(request):
    dep_output = '/home/shoval/repos/openU/hebrew-dependency-viewer/treeFetcher/parsing_handler/yapproj/src/yap/data/dep_output.conll'
    lattices = ''
    query = ""
    pos = ""
    relations = ""
    segments = ''
    morph = ''
    feedback = "thank you for your feedback"
    if request.method == 'GET':
        form = UtteranceForm
    else:
        form = UtteranceForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data.get('utterance')
            parsing = parse_sentence(query)
            parsing.wait()
            segments = segment_query()
            pos = pos_tagger()
            morph = morphological_analyzer()
            relations = show_dependencies()
            lattices_output = '/home/shoval/repos/openU/hebrew-dependency-viewer/treeFetcher/parsing_handler/yapproj/src/yap/data/lattices.conll'
            with open(lattices_output) as file:
                lattices = file.read().replace("\t", "      ")
    return render(request, "index.html", {'form': form, 'pos': pos, 'morph': morph, 'relations': relations, 'segments': segments, 'query': query, 'lattices': lattices, 'feedback': feedback})

def submit_conll(request):
    query = ""
    pos = ""
    relations = ""
    segments = ""
    morph = ''
    if request.method == 'GET':
        form = ConllForm
    else:
        form = ConllForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data.get('utterance')
            segments = segment_query(query)
            pos = pos_tagger(query)
            morph = morphological_analyzer(query)
            relations = show_dependencies(query.rstrip("\n"))
    return render(request, "conll-reader.html", {'form': form, 'pos': pos, 'relations': relations, 'segments': segments, 'query': query, 'morph': morph})

def relations(request):
    relations = DepCategory.objects.all()
    return render(request, "relations.html", {'relations': relations})

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
                send_mail(subject, everything, from_email, ['onlp.openu@gmail.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            sent = True
            return redirect('contact')
    return render(request, "contact.html", {'contact': contact, 'sent': sent})


def handler404(request):
    response = render('404.html', {}, context_instance=RequestContext(request))
    response.status_code = 404
    return response