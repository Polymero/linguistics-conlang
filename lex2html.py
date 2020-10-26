# Imports
import numpy as np
import pandas as pd
import argparse

# Initialise Parser
parser = argparse.ArgumentParser(description='Proto-Language Lexicon')
# Mode Parameters
parser.add_argument('type', type=str, action='store', metavar='action mode',
                    help='Please see README.md or github.com/Polymero/linguistics-conlang for help.')
# Return 'help' information if parsing not succesful
try:
    args = parser.parse_args()
except TypeError:
    parser.print_help()
# Parser variables
type    = args.type

# Import the correct lexicon.csv using Pandas
if type == 'lex':
    lex = pd.read_csv('./data/iskeelis.tsv', delimiter='\t')
elif type == 'evo':
    lex = pd.read_csv('./data/evolved.tsv', delimter='\t')
else:
    raise ValueError('Type not recognised, please use lex or evo.')
lex = lex.replace(np.nan, ' ', regex=True)

# Defined order of the alphabet
alphabet = ['a', 'á', 'b', 'c', 'd', 'e', 'é', 'f', 'g', 'h', 'i', 'í', 'j', 'k', 'l', 'hl',
            'm', 'n', 'o', 'ó', 'p', 'q', 'r', 's', 'sh', 't', 'tl', 'ch', 'u', 'v',
            'w', 'x', 'y', 'z']


# Print table
print('<table class="tg" style="undefined;table-layout: fixed; width: 903px">')
print('<colgroup>')
print('<col style="width: 301px">')
print('<col style="width: 301px">')
print('<col style="width: 301px">')
print('</colgroup>')
print('<tbody>')
# For each letter in the alphabet
for i in range(len(alphabet)):
    if alphabet[i] == 'h':
        sublex = lex[(lex['Orthography'].astype(str).str[0] == 'h') &
                     (lex['Orthography'].astype(str).str[1] == 'l')]
    elif alphabet[i] == 'hl':
        sublex = lex[(lex['Orthography'].astype(str).str[0] == 'h') &
                     (lex['Orthography'].astype(str).str[1] == 'l')]
    elif alphabet[i] == 's':
        sublex = lex[(lex['Orthography'].astype(str).str[0] == 's') &
                     (lex['Orthography'].astype(str).str[1] != 'h')]
    elif alphabet[i] == 'sh':
        sublex = lex[(lex['Orthography'].astype(str).str[0] == 's') &
                     (lex['Orthography'].astype(str).str[1] == 'h')]
    elif alphabet[i] == 't':
        sublex = lex[(lex['Orthography'].astype(str).str[0] == 't') &
                     (lex['Orthography'].astype(str).str[1] != 'l')]
    elif alphabet[i] == 'tl':
        sublex = lex[(lex['Orthography'].astype(str).str[0] == 't') &
                     (lex['Orthography'].astype(str).str[1] == 'l')]
    elif alphabet[i] == 'ch':
        sublex = lex[lex['Orthography'].astype(str).str[0] == 'c']
    else:
        sublex = lex[lex['Orthography'].astype(str).str[0] == alphabet[i]]

    # Print section
    if len(sublex.index) != 0:
        print('<tr>')
        print('<td class="tg-wp8o" colspan="3">{0}</td>'.format(alphabet[i]))
        print('</tr>')

        j = 0
        for index, entry in sublex.iterrows():
            if j % 3 == 0:
                print('<tr>')
            print('<td class="tg-73oq"><span style="font-weight:bold;color:#3166FF">{0}</span> [{1}]<br>    <span style="font-style:italic">{2}.</span> {3}</td>'.format(entry['Orthography'], entry['IPA'], entry['Class'], entry['Description'].lower()))
            if j % 3 == 2:
                print('</tr>')
            j += 1

print('</tbody>')
print('</table>')
