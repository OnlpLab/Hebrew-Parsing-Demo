import requests
import json
import re
import pandas as pd

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
    u = u.replace('. ', '.  ')
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
            pos.append({'token': lemma[2], 'xpos': lemma[3]})
    return pos

def get_lemmas(conll):
    lemmas = conll_to_list(conll)
    lemmas = [{'token': l[1], 'lemma': l[2]} for l in lemmas]
    return lemmas

def parse_lattice(lattices):
    lattice_list_of_dicts = []
    for row in lattices.split('\n'):
        row = row.split('\t')
        if len(row) > 7:
            lattice_list_of_dicts.append({"from": row[0], "to": row[1], "form": row[2], "lemma": row[3], "postag": row[4],
                              "features": row[6].replace("|", ","), "token_number": row[7]})
    return lattice_list_of_dicts

def morphological_analyzer(conll):
    lemmas = conll_to_list(conll)
    morph = []
    for lemma in lemmas:
        if (lemma[4] != "PUNCT") and ('-' not in lemma[2]):
            morph.append({'token': lemma[2], 'feats': lemma[6].replace("|", "\t\t").replace("_", "\t")})
    return morph


def show_dependencies(conll):
    lemmas = conll_to_list(conll)
    start_indices = [x for x in range(len(lemmas)) if lemmas[x][0] == '1']
    sentences = []
    for x in range(len(start_indices)-1):
        sentences.append(lemmas[start_indices[x]:start_indices[x+1]])
    last_sentence = lemmas[start_indices[-1]:]
    sentences.append(last_sentence)
    trees = []
    for sent in sentences:
        dependencies = []
        for y in range(len(sent)):
            if '-' not in sent[y][0]:
                relation = sent[y][7]
                head_index = sent[y][6]
                head_lemma = "root"
                self_lemma = sent[y][1]
                self_index = sent[y][0]
                for x in range(len(sent)):
                    if sent[x][0] == head_index:
                        head_lemma = sent[x][1]
                        break
                dependency_row = "%s(%s-%s, %s-%s)" %(relation, self_lemma, self_index, head_lemma, head_index)
                dependency = {'relation': relation, 'self_lemma': self_lemma, 'self_index': self_index,
                            'head_lemma': head_lemma, 'head_index': head_index, 'dep_row': dependency_row}
                dependencies.append(dependency)
        trees.append(dependencies)
        # tree = "\n".join(dependencies)
        # tree += "\n"
        # trees.append(tree)
    # return "\n".join(trees)
    return trees


if __name__ == "__main__":
    utterance = "שלום,  שנה טובה לכולם"
    parsed = parse_sentence(utterance)
    # print(utterance)