import subprocess
import io


yap = 'treeFetcher/yap_run.sh'
yap_nett = 'home/shoval/repos/openU/hebrew-dependency-viewer/treeFetcher/parsing_handler/yapproj/src/yap/yap'
dep_output = '/home/shoval/repos/openU/hebrew-dependency-viewer/treeFetcher/parsing_handler/yapproj/src/yap/data/dep_output.conll'

"""
the input file should be
שלום
,
היום
יום
יפה
.

"""

def create_input_raw(utterance):
    seperated = utterance.split(" ")
    # '/home/shoval/repos/openU/hebrew-dependency-viewer/treeFetcher/parsing_handler/yapproj/src/yap/data'
    input_path = '/home/shoval/repos/openU/hebrew-dependency-viewer/treeFetcher/parsing_handler/yapproj/src/yap/data/input.raw'
    with open(input_path, 'w') as file:
        file.write('\n'.join(seperated))
        file.write("\n\n")
    return input_path


def parse_sentence(utterance):
    create_input_raw(utterance)
    parsing = subprocess.Popen(yap, shell=True)
    parsing.wait()
    return parsing


conll_placeholder = """1	אכן	אכן	ADV	ADV	_	4	advmod	_	SpaceAfter=No
2	,	,	PUNCT	PUNCT	_	4	punct	_	_
3	כך	כך	ADV	ADV	_	4	advmod	_	_
4	עשתה	עשה	VERB	VERB	Gender=Fem|HebBinyan=PAAL|Number=Sing|Person=3|Tense=Past|Voice=Act	0	root	_	_
5	חטיבת	חטיבה	NOUN	NOUN	Definite=Cons|Gender=Fem|Number=Sing	4	nsubj	_	_
6	"	"	PUNCT	PUNCT	_	7	punct	_	SpaceAfter=No
7	הראל	הראל	PROPN	PROPN	_	5	flat:name	_	SpaceAfter=No
8	"	"	PUNCT	PUNCT	_	7	punct	_	SpaceAfter=No
9	.	.	PUNCT	PUNCT	_	4	punct	_	_"""

def conll_to_list(utterance=None):
    if utterance==None:
        with open(dep_output, 'r') as parse:
            lemmas = []
            for line in parse.readlines()[0:-1]:
                parts = [part for part in line.split("\t")]
                lemmas.append(parts)
    else:
        lemmas = []
        for line in utterance.split("\n"):
            parts = [part for part in line.split("\t")]
            lemmas.append(parts)
    return lemmas


def segment_query(utterance=None):
    lemmas = conll_to_list(utterance)
    pos = []
    for lemma in lemmas:
        if '-' not in lemma[0]:
            pos.append(lemma[1])
    return " ".join(pos)

def pos_tagger(utterance=None):
    lemmas = conll_to_list(utterance)
    pos = []
    for lemma in lemmas:
        if (lemma[3] != "PUNCT") and ('-' not in lemma[0]):
            pos.append("%s %s" % (lemma[1], lemma[3]))
    return "\n".join(pos)


def morphological_analyzer(utterance=None):
    lemmas = conll_to_list(utterance)
    morph = []
    for lemma in lemmas:
        if (lemma[3] != "PUNCT") and ('-' not in lemma[0]):
            morph.append("%s\t\t%s\t\t" % (lemma[1], lemma[5].replace("|", "\t\t").replace("_", "\t")))
    return "\n".join(morph)


def show_dependencies(utterance=None):
    lemmas = conll_to_list(utterance)
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




