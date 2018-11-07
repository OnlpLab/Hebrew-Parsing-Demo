import requests
import json
import re

# curl -s -X GET -H 'Content-Type: application/json' -d'{"text": "גנן גידל דגן בגן  "}' localhost:8000/yap/heb/pipeline | jq -r '.dep_tree' | sed -e 's/\\t/\t/g' -e 's/\\n/\n/g'
url = "http://onlp.openu.org.il:8000/yap/heb/joint"

def call_yap_webapi(utterance) -> dict:
    data = '''{"text": "%s  "}''' % utterance
    response = requests.post(url,
                             data=data.encode('utf-8'),
                             headers={'Content-type': 'applications/json'})
    return response.json()
#
def space_punctuation(utterance):
    u = re.sub('([!#$%&\()*+,-./:;<=>?@\^_|~])', r' \1 ', utterance)
    u = re.sub('(\s[\'\"`])', r' \1 ', u)  # beginning of quote
    u = re.sub('([\'\"`]\s)', r' \1 ', u)  # end of quote
    u = re.sub('(^[\'\"`])', r' \1 ', u)  # sentence starts with quote
    u = re.sub('([\'\"`]$)', r' \1 ', u)  # sentence ends with quote
    u = re.sub('(\w{1,3})([\'\"`])(\w{2,})', r' \2 \1\3', u)  # quote start after morpheme (but not acronyms)
    #  e.g. גנן גידל דגן ב"גן הירק". The quote moves to left word boundary.

    u = re.sub(r'([^\\])([\"])', r'\1\\\2', u)
    u = re.sub(r' +', ' ', u)
    return u





def parse_sentence(utterance) -> dict:
    return call_yap_webapi(space_punctuation(utterance))


def conll_to_list(conll):
    lemmas = []
    for line in conll.split("\n"):
        if not line:
            continue
        elif line == '\"':
            continue
        parts = [part for part in line.split("\t")]
        lemmas.append(parts)
    return lemmas


def segment_query(conll):
    lemmas = conll_to_list(conll)
    pos = []
    for lemma in lemmas:
        if '-' not in lemma[0]:
            pos.append(lemma[1])
    return "  ".join(pos)

def pos_tagger(conll):
    lemmas = conll_to_list(conll)
    pos = []
    for lemma in lemmas:
        if (lemma[3] != "PUNCT") and ('-' not in lemma[0]):
            pos.append("%s %s" % (lemma[2], lemma[4]))
    return "\n".join(pos)

def morphological_analyzer(lattice):
    lemmas = conll_to_list(lattice)
    morph = []
    for lemma in lemmas:
        if (lemma[4] != "PUNCT") and ('-' not in lemma[2]):
            morph.append("%s\t\t%s\t\t" % (lemma[2], lemma[6].replace("|", "\t\t").replace("_", "\t")))
    return "\n".join(morph)


def show_dependencies(conll):
    lemmas = conll_to_list(conll)
    dependencies = []
    for line in lemmas:
        if (line[3] != "PUNCT") and ('-' not in line[0]):
            relation = line[7]
            head_index = line[6]
            head_lemma = "root"
            for subline in lemmas:
                if subline[0] == head_index:
                    head_lemma = subline[1]
            self_lemma = line[1]
            self_index = line[0]
            dependency = "%s(%s-%s, %s-%s)" %(relation, self_lemma, self_index, head_lemma, head_index)
            dependencies.append(dependency)
    return "\n".join(dependencies)


if __name__ == "__main__":
    utterance = "שלום ,  שנה טובה לכולם"
    parsed = parse_sentence(utterance)
    print(parsed)