from .conll_api_fetcher import parse_sentence, morphological_analyzer, show_dependencies, segment_query, pos_tagger, get_lemmas, parse_lattice
from .spmrl_to_ud import Convert_SPMRL_to_UD, basic_features, basic_pos, entire_line_pos_conversion
from django.shortcuts import render, redirect
from .forms import UtteranceForm
import time
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponseRedirect, HttpResponse
import logging


logger = logging.getLogger(__name__)

def submit_utterance(request):
    lattices = ''
    query = ""
    pos = ""
    relations = ""
    segments = ''
    morph = ''
    lemmas = ''
    lattice_table = ''
    converted = ''

    if request.method == 'GET':
        form = UtteranceForm
    else:
        form = UtteranceForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data.get('utterance')
            parse_data = parse_sentence(query)
            try:
                lattice = parse_data['md_lattice']
                lattices = parse_data['ma_lattice']
                lattice_table = parse_lattice(lattices)
                conll = parse_data['dep_tree']
                converted_conll = Convert_SPMRL_to_UD(conll)
                # TODO: fix conversion (see notes in spmrl_to_ud.py) and uncomment the lines below + in index.html
                converted_conll.apply_conversions(feats=basic_features, simple_pos=basic_pos,
                                                  complex_pos_conversions=entire_line_pos_conversion)
                converted = converted_conll.segmented_sentence
                segments = segment_query(conll)
                pos = pos_tagger(conll)
                relations = show_dependencies(conll)
                lemmas = get_lemmas(conll)
                morph = morphological_analyzer(lattice)
                converted = converted[['FORM', 'LEMMA', 'UPOS', 'FEATS']].to_dict(orient='index')
                converted = [v for v in converted.values()]
            except KeyError:
                pos = "error"
                send_bad_input(query)
    return render(request, "index.html", {'form': form, 'pos': pos, 'lemmas': lemmas, 'morph': morph,
                                          'relations': relations, 'segments': segments, 'query': query,
                                          'lattices': lattice_table,
                                          'converted': converted
                                          })


def send_bad_input(query):
    content = "timestamp: {}\nquery: {}".format(time.asctime(), query)
    try:
        logger.error("crash report says: \n{}".format(content))
        # send_mail("crash report onlp demo {}".format(time.time()), content, 'onlp.openu@gmail.com', ['shovatz@gmail.com'])
    except BadHeaderError:
        return HttpResponse('Invalid header found.')

def send_wrong_parse():
    pass

def send_correct_parse():
    pass

