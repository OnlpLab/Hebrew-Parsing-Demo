"""
Input can be either a string or a csv file with conll-x format. If csv, please provide a filepath.
"""
import pandas as pd
import numpy as np
import csv
from tqdm import trange, tqdm
# from tqdm import tqdm_notebook as tqdm

class Convert_SPMRL_to_UD():

    def __init__(self, conll=None, filepath=None):
        self.conll = conll
        self.filepath = filepath
        if self.conll:
            self.df = self.create_df_from_conll_formatted_string()
        elif self.filepath:
            self.df = self.create_df_from_conll_file(filepath=filepath)
        self.pronouns = {
             'suf_gen=F|suf_gen=M|suf_num=P|suf_per=1': '_אנחנו',
             'suf_gen=F|suf_gen=M|suf_num=S|suf_per=1': '_אני',
             'suf_gen=M|suf_num=S|suf_per=2': '_אתה',
             'suf_gen=F|suf_num=S|suf_per=2': '_את',
             'suf_gen=M|suf_num=P|suf_per=2': '_אתם',
             'suf_gen=F|suf_num=P|suf_per=2': '_אתן',
             'suf_gen=F|suf_num=P|suf_per=3': '_הן',
             'suf_gen=F|suf_num=S|suf_per=3': '_היא',
             'suf_gen=M|suf_num=P|suf_per=3': '_הם',
             'suf_gen=M|suf_num=S|suf_per=3': '_הוא'
        }
        self.segmented_sentence = self.segment_df()


    def create_df_from_conll_file(self, filepath):
        treebank = []
        columns = ['ID', 'FORM', 'LEMMA', 'UPOS', 'XPOS', 'FEATS', 'HEAD', 'DEPREL', 'DEPS', 'MISC']
        try:
            df = pd.read_csv(filepath, sep='\t', header=None, names=columns, na_filter=False, quoting=csv.QUOTE_NONE)
        except:
            with open(filepath, 'r') as source:
                for line in source.readlines():
                    if len(line.split('\t')) == 10:
                        treebank.append(tuple(line.strip().split('\t')))
                    elif len(line.split('\t')) == 1:
                        treebank.append((line.strip(), '', '', '', '', '', '', '', '', ''))
                df = pd.DataFrame(data=treebank, columns=columns)
        return df

    def create_df_from_conll_formatted_string(self):
        rows = []
        conll = self.conll.split('\n')
        for line in conll:
            cols = line.split('\t')
            if len(cols) > 1:
                rows.append({'ID': cols[0], 'FORM': cols[1], 'LEMMA': cols[2], 'UPOS': cols[3], 'XPOS': cols[4],
                             'FEATS': cols[5], 'HEAD': cols[6], 'DEPREL': cols[7], 'DEPS': cols[8], 'MISC': cols[9]})
        df = pd.DataFrame(rows)
        return df

    def segment_df(self):
        output_df = pd.DataFrame(
            columns=['ID', 'FORM', 'LEMMA', 'UPOS', 'XPOS', 'FEATS', 'HEAD', 'DEPREL', 'DEPS', 'MISC',
                     ])
        print("segmenting sentence...")
        for i, row in tqdm(self.df.iterrows(), total=self.df.shape[0]):
            suffix_feats = "|".join([x for x in row['FEATS'].split("|") if 'suf' in x])
            noun_feats = "|".join([x for x in row['FEATS'].split("|") if 'suf' not in x])
            clean_suffix_feats = "|".join([x.replace("suf_", "") for x in row['FEATS'].split("|") if 'suf' in x])
            if 'suf_' in row['FEATS'] and row['UPOS'] == 'NN':
                output_df = output_df.append({'ID': row['ID'], 'FORM': row['LEMMA'] + '_', 'LEMMA': row['LEMMA'],
                                              'UPOS': 'NOUN', 'XPOS': 'NOUN',
                                              'FEATS': 'Definite=Def|' + noun_feats + '|xx_UD=Seg',
                                              'HEAD': row['HEAD'], 'DEPREL': row['DEPREL'], 'DEPS': row['DEPS'],
                                              'MISC': row['MISC']}, ignore_index=True)

                output_df = output_df.append({'ID': 0, 'FORM': '_של_', 'LEMMA': 'של', 'UPOS': 'ADP',
                                              'XPOS': 'ADP', 'FEATS': '_' + '|xx_UD_REL=case:gen',
                                              'HEAD': int(row['ID']) + 2,
                                              'DEPREL': row['DEPREL'], 'DEPS': row['DEPS'], 'MISC': row['MISC']}, ignore_index=True)

                output_df = output_df.append(
                    {'ID': 0, 'FORM': self.pronouns[suffix_feats], 'LEMMA': 'הוא', 'UPOS': 'PRON',
                     'XPOS': 'PRON',
                     'FEATS': "Case=Gen|" + clean_suffix_feats + "|PronType=Prs" + '|xx_UD_REL=nmod:poss',
                     'HEAD': int(row['ID']) + 2, 'DEPREL': row['DEPREL'], 'DEPS': row['DEPS'],
                     'MISC': row['MISC']}, ignore_index=True)


            # #TODO: check why this is here
            elif row['XPOS'] == 'S_PRN':
                if output_df.loc[i-1]['XPOS'] == 'AT':
                    output_df.at[i - 1, 'FEATS'] = 'Case=Acc'
                elif output_df.loc[i - 1]['LEMMA'] == 'של':
                    output_df.at[i - 1, 'FEATS'] = 'Case=Gen'
                elif output_df.loc[i - 1]['XPOS'] == 'IN':
                    output_df.at[i - 1, 'FEATS'] = ''
                output_df = output_df.append(
                {'ID': row['ID'], 'FORM': '_' + row['LEMMA'], 'LEMMA': row['LEMMA'], 'UPOS': 'PRON',
                 'XPOS': 'PRON', 'FEATS': row['FEATS'] + '|PronType=Prs', 'HEAD': row['HEAD'],
                 'DEPREL': row['DEPREL'], 'DEPS': row['DEPS'], 'MISC': row['MISC']}, ignore_index=True)


                # if output_df.loc[i - 1]['FEATS']:
                #     print("feats")
                #     prev_feats = output_df.loc[i - 1]['FEATS'] + '|'
                # else:
                #     print(self.df.loc[i-1])
                #     print(self.df.loc[i])
                #     print("no feats")
                #     prev_feats = output_df.loc[i - 1]['FEATS']
                # if prev_feats == '_|':
                #     prev_feats = ''
                # output_df = output_df.append(
                # {'ID': row['ID'], 'FORM': '_' + row['LEMMA'], 'LEMMA': row['LEMMA'], 'UPOS': 'PRON',
                #  'XPOS': 'PRON', 'FEATS': prev_feats + 'PronType=Prs', 'HEAD': row['HEAD'],
                #  'DEPREL': row['DEPREL'], 'DEPS': row['DEPS'], 'MISC': row['MISC']}, ignore_index=True)


                # output_df.at[i - 1, 'XPOS'] = 'ADP'
                # output_df.at[i - 1, 'FORM'] += '_'
                # output_df.at[i - 1, 'FEATS'] = 'Case=Gen' # needs recheck - S_PRN seems mostly dative

            elif row['XPOS'] == 'DTT' or row['XPOS'] == 'DT':
                if 'suf_' in row['FEATS']:
                    output_df = output_df.append(
                        {'ID': row['ID'], 'FORM': row['FORM'], 'LEMMA': row['LEMMA'], 'UPOS': 'NOUN',
                         'XPOS': 'NOUN', 'FEATS': row['FEATS'], 'HEAD': row['HEAD'],
                         'DEPREL': row['DEPREL'], 'DEPS': row['DEPS'], 'MISC': row['MISC']}, ignore_index=True)

                    output_df = output_df.append(
                        {'ID': 0, 'FORM': "_" + self.pronouns[suffix_feats], 'LEMMA': 'הוא', 'UPOS': 'PRON',
                         'XPOS': 'PRON',
                         'FEATS': "Case=Gen|" + clean_suffix_feats + "|PronType=Prs" + '|xx_UD_REL=nmod:poss',
                         'HEAD': int(row['ID']) + 1, 'DEPREL': row['DEPREL'], 'DEPS': row['DEPS'],
                         'MISC': row['MISC']}, ignore_index=True)

                else:
                    output_df = output_df.append(row, ignore_index=True)
            else:
                output_df = output_df.append(row, ignore_index=True)
        return output_df

    def apply_conversions(self, feats=None, simple_pos=None, complex_pos_conversions=None):

        def change_previous_row(row):
            """this method doesn't work yet. reise when the
            rest of the segmentation is fixed"""
            feats = row['FEATS']
            xpos = row['XPOS']
            upos = xpos
            prev = row.name - 1
            if xpos == 'PRON' and feats == 'PronType=Prs':
                if prev > 0:
                    if self.df.at[prev, 'XPOS'] == 'ADP':
                        try:
                            prev_feats = self.df.at[prev, 'FEATS']
                        except:
                            print(prev)
                        self.segmented_sentence.at[prev, 'XPOS'] = 'ADP'
                        self.segmented_sentence.at[prev, 'FEATS'] = 'Case=Gen'
                        upos = 'PRON'
                        feats += '|PronType=Prs'
                    else:
                        print(self.df.at[prev, 'XPOS'])
                else:
                    print("here: name", row.name)
            else:
                print(xpos)
            return pd.Series([upos, feats])

        # self.segmented_sentence[['UPOS', 'FEATS']] = self.segmented_sentence.apply(change_previous_row, axis=1)

        def simple_features_conversion(column, conversions):
            for old, new in conversions.items():
                column = column.replace(old, new)

            return column

        def pos_conversion(column, conversions):
            if column in conversions:
                return conversions[column]
            else:
                return column



        def pos_convert_entire_line(row, conversions):
            xpos = row['XPOS']
            form = row['FORM']
            feats = row['FEATS']
            #     if xpos in conversions:
            if xpos in conversions:
                if 'concat' in xpos:
                    if xpos['concat'] == 'before':
                        form = '_' + form
                    elif xpos['concat'] == 'after':
                        form += '_'
                    else:
                        form = '_' + form + '_'
                upos = conversions[xpos]['pos']
                if conversions[xpos]['feats'] == 'feats':
                    feats = row['FEATS']
                elif conversions[xpos]['feats']['old'] == '_':
                    feats = conversions[xpos]['feats']['new']
                elif conversions[xpos]['feats']['old'] == 'feats+':
                    if len(row['FEATS']) > 2:
                        feats = row['FEATS'] + conversions[xpos]['feats']['new']
                    else:
                        feats = conversions[xpos]['feats']['new'][1:]
                elif conversions[xpos]['feats']['old'] == '+feats':
                    feats = conversions[xpos]['feats']['new'] + row['FEATS']
                elif conversions[xpos]['feats']['old'] == '+feats+':
                    feats = conversions[xpos]['feats']['new'][0] + row['FEATS'] + conversions[xpos]['feats']['new'][1]
                return pd.Series([upos, form, feats])
            else:
                return pd.Series([row['UPOS'], row['FORM'], row['FEATS']])



        if feats:
            self.segmented_sentence.loc[:, 'FEATS'] = self.segmented_sentence['FEATS'].apply(
                lambda x: simple_features_conversion(x, feats))

        if simple_pos:
            self.segmented_sentence.loc[:, 'UPOS'] = self.segmented_sentence['UPOS'].apply(
                lambda x: pos_conversion(x, simple_pos))

        if complex_pos_conversions:
            self.segmented_sentence[['UPOS', 'FORM', 'FEATS']] = self.segmented_sentence.apply(
                lambda x: pos_convert_entire_line(x, complex_pos_conversions), axis=1)

        # return self.df

basic_features = {'suf_': '', 'gen=F|gen=M': 'Gender=Fem,Masc', 'gen=F': 'Gender=Fem', 'gen=M': 'Gender=Masc',
                  'num=S': 'Number=Sing', 'num=P': 'Number=Plur',
                  'per=A': 'Person=1,2,3', 'per=': 'Person=',
                  'tense=BEINONI': 'VerbForm=Part', 'tense=TOINFINITIVE': 'VerbForm=Inf',
                  'tense=IMPERATIVE': 'Mood=Imp',
                  'tense=PAST': 'Tense=Past', 'tense=FUTURE': 'Tense=Fut'
                  }

basic_pos = {
    'IN': 'ADP', 'NNP': 'PROPN', 'JJ': 'ADJ', 'NN': 'NOUN', 'VB': 'VERB', 'RB': 'ADV', 'NCD': 'NUM', 'NEG': 'ADV',
    'PREPOSITION': 'ADP', 'REL': 'SCONJ', 'COM': 'SCONJ', 'CONJ': 'CCONJ', 'POS': 'ADP', 'PRP': 'PRON',
    'yyCLN': 'PUNCT', 'yyCM': 'PUNCT', 'yyDASH': 'PUNCT', 'yyDOT': 'PUNCT', 'yyELPS': 'PUNCT', 'yyEXCL': 'PUNCT',
    'yyLRB': 'PUNCT', 'yyQM': 'PUNCT', 'yyQUOT': 'PUNCT', 'yyRRB': 'PUNCT', 'yySCLN': 'PUNCT', 'ZVL': 'X'
}

entire_line_pos_conversion = {
    'AT': {'pos': 'ADP', 'feats': {'old': '_', 'new': 'Case=Acc|xx_UD_REL=case:acc'}},
    'BN': {'pos': 'VERB', 'feats': {'old': 'feats+', 'new': "|VerbForm=Part"}},
    'BNT': {'pos': 'VERB', 'feats': {'old': '+feats+', 'new': ['Definite=Cons|', '|VerbForm=Part']}},
    'CD': {'pos': 'NUM', 'feats': 'feats'},
    'CDT': {'pos': 'NUM', 'feats': {'old': '+feats', 'new': "Definite=Cons|"}},
    'NNT': {'pos': 'NOUN', 'feats': {'old': '+feats', 'new': "Definite=Cons|"}},
    'COP': {'pos': 'AUX', 'feats': {'old': 'feats+', 'new': "|VerbType=Cop|VerbForm=Part"}},
    'DEF': {'pos': 'DET', 'feats': {'old': '_', 'new': 'PronType=Art'}, 'concat': 'after'},
    'EX': {'pos': 'VERB', 'feats': {'old': '_', 'new': 'HebExistential=True'}},
    'P': {'pos': 'ADV', 'feats': {'old': '_', 'new': 'Prefix=True|xx_UD_REL=compound:affix'}},
    'DUMMY_AT': {'pos': 'ADP', 'feats': {'old': '_', 'new': 'Case=Acc|xx_UD_REL=case:acc'}},
    'JJT': {'pos': 'ADJ', 'feats': {'old': '+feats', 'new': 'Definite=Cons|'}},
    'MD': {'pos': 'AUX', 'feats': {'old': 'feats+', 'new': '|VerbType=Mod'}},
    'QW': {'pos': 'ADV', 'feats': {'old': '_', 'new': 'PronType=Int'}},
    'TEMP': {'pos': 'SCONJ', 'feats': {'old': '_', 'new': 'Case=Tem|xx_UD_REL=mark'}},
    'DTT': {'pos': 'DET', 'feats': {'old': '_', 'new': 'Definite=Cons'}},
    'S_ANP': {'pos': 'PRON', 'feats': {'old': '+feats+', 'new': ['Case=Acc|', '|PronType=Prs']}},
    'S_PRP': {'pos': 'PRON', 'feats': {'old': 'feats+', 'new': '|PronType=Prs|Reflex=Yes'}}
}
#
if __name__ == '__main__':
#     filepath_spmrl_dev = './data/spmrl-treebank/dev_hebtb-gold.conll'
#     filepath_spmrl_train = './data/spmrl-treebank/train_hebtb-gold.conll'
#     filepath_spmrl_test = './data/spmrl-treebank/test_hebtb-gold.conll'
#
#     filepath_ud_dev = './data/ud-treebank/he_htb-ud-dev.conllu'
#     filepath_ud_train = './data/ud-treebank/he_htb-ud-train.conllu'
#     filepath_ud_test = './data/ud-treebank/he_htb-ud-test.conllu'
#
    ganan = """
1	גנן	גנן	NN	NN	gen=M|num=S	2	subj	_	_
2	גידל	גידל	VB	VB	gen=M|num=S|per=3|tense=PAST	0	ROOT	_	_
3	דגנים	דגן	NN	NN	gen=M|num=P	2	obj	_	_
4	ב	ב	PREPOSITION	PREPOSITION		2	prepmod	_	_
5	גנו	גן	NN	NN	gen=M|num=S|suf_gen=M|suf_num=S|suf_per=3	4	pobj	_	_
    """
    converter = Convert_SPMRL_to_UD(conll=ganan)
    # converter = Convert_SPMRL_to_UD(filepath=filepath_spmrl_dev)
#     base_df = converter.df
#     print(base_df)
#     # seg_df = converter.segmented_sentence
#
#
    converter.apply_conversions(feats=basic_features, simple_pos=basic_pos, complex_pos_conversions=entire_line_pos_conversion)
#
#     # print(converter.segmented_sentence[])
#     # columns = ['ID', 'FORM', 'LEMMA', 'UPOS', 'XPOS', 'FEATS', 'HEAD', 'DEPREL', 'DEPS', 'MISC']
#     # converter.segmented_sentence.to_csv('./data/check.conllu', sep='\t', columns=columns, quoting=csv.QUOTE_NONE)
