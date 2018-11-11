from django import forms


class UtteranceForm(forms.Form):
    utterance = forms.CharField(max_length=600, label='Utterance', widget=forms.Textarea(attrs={
        'placeholder': 'למשל, גנן גידל דגן בגן',
        'rows': 5,
        'cols': 100}))

    annotation_options = ((None, "Choose Annotation"), ('segmentation', 'Segmentation'), ('pos', 'Part-of_speech Tags'),
                          ('dependency', 'Dependency Parse'),)
    # annotation = forms.MultipleChoiceField(choices=annotation_options)
    filename_options = ((None, "Choose type of output"), ('input', 'Input'), ('lattices', 'All possible lattices'),
                        ('output', 'The most likely lattice'), ('dependency', 'Dependency Parse'),)
    # filename = forms.ChoiceField(choices=filename_options, label="Type of output")


conll_placeholder = """
1	אכן	אכן	ADV	ADV	_	4	advmod	_	SpaceAfter=No
2	,	,	PUNCT	PUNCT	_	4	punct	_	_
3	כך	כך	ADV	ADV	_	4	advmod	_	_
4	עשתה	עשה	VERB	VERB	Gender=Fem|HebBinyan=PAAL|Number=Sing|Person=3|Tense=Past|Voice=Act	0	root	_	_
5	חטיבת	חטיבה	NOUN	NOUN	Definite=Cons|Gender=Fem|Number=Sing	4	nsubj	_	_
6	"	"	PUNCT	PUNCT	_	7	punct	_	SpaceAfter=No
7	הראל	הראל	PROPN	PROPN	_	5	flat:name	_	SpaceAfter=No
8	"	"	PUNCT	PUNCT	_	7	punct	_	SpaceAfter=No
9	.	.	PUNCT	PUNCT	_	4	punct	_	_
"""

class ConllForm(forms.Form):
    utterance = forms.CharField(label='Utterance', widget=forms.Textarea(attrs={
        'placeholder': conll_placeholder,
        'rows': 10,
        'cols': 100}), help_text="Please insert the conll-U file content of a single sentence, like the example below:")


class MyForm(forms.Form):
  def as_contact(self):
    return self._html_output(
        normal_row='<p%(html_class_attr)s> %(label)s <br> %(field)s %(help_text)s </p>',
        error_row='%s',
        row_ender='</p>',
        help_text_html=' <span class="helptext">%s</span>',
        errors_on_separate_row=True)

class ContactForm(MyForm):
    contact_name = forms.CharField(required=True, label="Name")
    contact_email = forms.EmailField(required=True, label="Email")
    subject = forms.CharField(required=True, label='Subject')
    message = forms.CharField(required=True, widget=forms.Textarea, label='Message')
