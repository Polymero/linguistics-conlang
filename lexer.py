# Imports
# Internal
import argparse
import warnings
# External
import numpy as np
import pandas as pd
from matplotlib.pyplot import figure, show
# Matplotlib config
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})

# Paths
isk_path = r'C:\Users\Nika\Python\data\iskeelis.csv'
evo_path = r'C:\Users\Nika\Python\data\evolved.csv'
fau_path = r'C:\Users\Nika\Python\data\hlaahu.csv'

# Suppress FutureWarning
warnings.simplefilter(action='ignore', category=FutureWarning)

# Initialise Parser
parser = argparse.ArgumentParser(description='Proto-Language Lexicon')
# Mode Parameters
parser.add_argument('mode', type=str, action='store', metavar='action mode',
                    help='Please see README.md or github.com/Polymero/linguistics-conlang for help.')
# Entry Parameters
parser.add_argument('-entry', type=str, default='', help='All-in-one entry (sep=\':\')')
parser.add_argument('-id', type=int, default=None, help='Index ID of entry')
parser.add_argument('-ax', type=str, default='', help='Search axis')
parser.add_argument('-ser', type=str, default='', help='Search')
parser.add_argument('-ran', type=int, default=0, help='Number of samples')
parser.add_argument('-i', type=int, default=0, help='Input Age')
parser.add_argument('-f', type=int, default=99, help='Output Age')

# Return 'help' information if parsing not succesful
try:
    args = parser.parse_args()
except TypeError:
    parser.print_help()

# Parser variables
mode    = args.mode
entry   = args.entry
id      = args.id
axis    = args.ax
search  = args.ser
ran_num = args.ran
age_i   = args.i
age_f   = args.f

#-------------------------------------------------------------------------------
# SUPPORT FUNCTIONS
#-------------------------------------------------------------------------------
def trans_ipa(ortho, lang='IS', age=0):
    '''RETURNS IPA FROM ORTHOGRAPHIC INPUT'''
    if lang.lower() == 'is':
        True
    else:
        raise ValueError('Language not recognised.')
    return ipa

def find_stress(ipa, lang='IS', age=0):
    '''RETURNS INDEX OF STRESSED SYLLABLE'''
    if lang.lower() == 'is':
        True
    else:
        raise ValueError('Language not recognised.')
    return stress

def evolver(path, entry, age_i, age_f, lang='IS'):
    '''RETURNS EVOLVED ENTRY'''
    if lang.lower() == 'is':
        True
    else:
        raise ValueError('Evolution path not recognised.')
    return evo


#-------------------------------------------------------------------------------
# MAIN FUNCTIONS
#-------------------------------------------------------------------------------
def add(path, entry):
    '''APPENDS ENTRY TO CORRESPONDING LEXICON'''
    try:
        lex = pd.read_csv(path, sep=r'\t', engine='python')
    except:
        raise ValueError('Error loading CSV.')

    if path == isk_path:
        # Split entry parameter
        ortho, fauja, age, type, desc = entry.split(':')
        # Get IPA
        ipa = trans_ipa(ortho, lang='IS', age=age)
        # Create entry dictionary
        ne = {
            'Orthography' : ortho,
            'IPA' : ipa,
            'Stress' : find_stress(ipa, lang='IS', age=age),
            'Hláhu' : fauja,
            'Age' : age,
            'Class' : type,
            'Description' : desc
        }

    elif path == fau_path:
        # Split entry parameter
        number, namedot, desc, ngstat = ocd.split(':')
        # Get syllables
        sylls = namedot.lower().split('.')
        # Create entry dictionary
        ne = {
            'NO.' : int(number),
            'Name' : namedot.replace('.', '').replace(' ', ''),
            'Nerlé' : sylls[0],
            'Óle' : ', '.join(sylls[1:]),
            'Description' : desc,
            'NG' : int(ngstat)
        }

    # Add entry to lexicon
    lex = lex.append(ne, ignore_index=True)
    lex.to_csv(lex_path, sep='\t', index=False)
    # Succes message
    print('\nSuccesfully logged the following entry:')
    print(pd.Series(ne))

def rem(path, id):
    '''REMOVES ENTRY FROM CSV ACCORDING TO ID'''
    try:
        lex = pd.read_csv(path, sep=r'\t', engine='python')
    except:
        raise ValueError('Error loading CSV.')
    # Drop row with index equal to given ID
    re = lex.iloc[id]
    lex = lex.drop(id, axis=0)
    lex.to_csv(path, sep='\t', index=False)
    # Succes message
    print('\nSuccesfully delogged the following entry:')
    print(pd.Series(re))

def lst(path, axis, search, ran_num):
    '''PRINTS (RANDOM) ENTRIES ACCORDING TO SEARCH'''
    try:
        lex = pd.read_csv(path, sep=r'\t', engine='python')
    except:
        raise ValueError('Error loading CSV.')
    # Set print options
    pd.set_option('display.expand_frame_repr', False)
    pd.set_option('display.max_rows', 999)
    # Apply search
    if (axis != '' and search != ''):
        plex = lex[lex[axis].str.lower().str.contains(search.lower())]
    else:
        plex = lex
    # Apply random sampling
    if ran_num > 0:
        plex = lex.sample(n=int(ran_num))
    # Print resulting DataFrame
    print(plex.sort_values('Orthography'))

#-------------------------------------------------------------------------------
# MODE FUNCTION
#-------------------------------------------------------------------------------
