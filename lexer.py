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

# Path Dictionary
path_dic = {
    # Language lexicons
    'IS' : r'C:\Users\Nika\Python\linguistics-conlang\data\iskeelis.csv',
    # Evolved lexicon
    'EVO' : r'C:\Users\Nika\Python\linguistics-conlang\data\evolved.csv',
    # Hláhu/Fauja lexicon
    'FAU' : r'C:\Users\Nika\Python\linguistics-conlang\data\hlaahu.csv'
}

# Suppress FutureWarning
warnings.simplefilter(action='ignore', category=FutureWarning)

# Initialise Parser
parser = argparse.ArgumentParser(description='Proto-Language Lexicon')
# Mode Parameters
parser.add_argument('mode', type=str, action='store', metavar='action mode',
                    help='Please see README.md or github.com/Polymero/linguistics-conlang for help.')
parser.add_argument('lang', type=str, action='store', metavar='language code')
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
lang    = args.lang
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
        # Replace digraphs
        ortho = ortho.replace('hl', 'H').replace('tl', 'L').replace('sh', 'S').replace('ch', 'C').replace('dh', 'D')
        ortho = ortho.replace('au', 'Á').replace('eu', 'É').replace('ou', 'Ó')
        # Split into syllables
        syllables = [list(x) for x in ortho.split('.')]
        # Replace characters accordingly
        for j in range(len(syllables)): # For each syllable
            syl = syllables[j]
            length = len(syl)
            for i in range(length): # For each letter
                if syl[i] == 'i':
                    syllables[j][i] = 'ɪ'
                elif syl[i] == 'í':
                    syllables[j][i] = 'i'
                elif syl[i] == 'á':
                    syllables[j][i] = 'aː'
                elif syl[i] == 'Á':
                    syllables[j][i] = 'aʊ'
                elif syl[i] == 'É':
                    syllables[j][i] = 'ɛʊ'
                elif syl[i] == 'Ó':
                    syllables[j][i] = 'ɔʊ'
                elif syl[i] == 'D':
                    syllables[j][i] = 'ð'
                elif syl[i] == 'n':
                    if i == length - 1:
                        if j != len(syllables) - 1: # /n/ to velar nasal
                            if syllables[j+1][0] in 'ghk':
                                syllables[j][i] = 'ŋ'
                elif syl[i] == 'r':
                    syllables[j][i] = 'ɾ'
                elif syl[i] == 'ŕ':
                    syllables[j][i] = 'ʀ'
                elif syl[i] == 'o':
                    syllables[j][i] = 'ɔ'
                elif syl[i] == 'ó':
                    syllables[j][i] = 'ɔː'
                elif syl[i] == 'e':
                    syllables[j][i] = 'ɛ'
                elif syl[i] == 'é':
                    syllables[j][i] = 'ɛː'
                elif syl[i] == 'q':
                    syllables[j][i] = 'ɣ'
                elif syl[i] == 'L':
                    syllables[j][i] = 'tɬ'
                elif syl[i] == 'H':
                    syllables[j][i] = 'ɬ'
                elif syl[i] == 'j':
                    if (i != 0) & (i != length - 1): # Parasitic /j/
                        syllables[j][i] = 'ʲ'
                elif syl[i] == 'S':
                    syllables[j][i] = 'ʃ'
                elif syl[i] == 'C':
                    syllables[j][i] = 'tʃ'
                elif syl[i] == "'":
                    syllables[j][i] = ''
                elif syl[i] == 'w':
                    syllables[j][i] = 'ʋ'
        # Paste characters back together
        for i in syllables:
            i.append('.')
        ipa = ''.join([char for syl in syllables for char in syl])
        ipa = ipa[:-1]
    # Raise error if language code not recognised
    else:
        raise ValueError('Language not recognised.')
    # Return transcribed orthography
    return ipa


def find_stress(ipa, lang='IS', age=0):
    '''RETURNS INDEX OF STRESSED SYLLABLE'''
    if lang.lower() == 'is':
        # Split into syllables
        sylls = ipa.split('.')
        # One syllable words
        if len(sylls) == 1:
            stress = -1
        # Stress on penultimate syllable, except if final syllable has a long vowel or /i/
        else:
            if ('ː' in sylls[-1] or 'i' in sylls[-1]):
                stress = -1
            else:
                stress = -2
    # Raise error if language code not recognised
    else:
        raise ValueError('Language not recognised.')
    # Return stress index
    return stress


def evolver(entry, age_i, age_f, lang='IS'):
    '''RETURNS EVOLVED ENTRY'''
    word = entry
    # Phoneme groups
    pgS = 'aeoui'                   # short vowels
    pgL = 'áéóí'                    # long vowels (and /i/)
    pgV = pgS + pgL                 # all vowels
    pgLiq = 'rljw'                  # liquids
    pgC = 'qwrtpsdfghjklzxcvbnm'    # all consonants
    # Check language code
    if lang.lower() == 'is':
        # AGE 0
        if (age_i <= 0 and age_f >= 0):
            # 0.1 /h/-dropping
            word = word.replace('hl','L').replace('h', '').replace('L', 'hl')
            # 0.2 Vowel hiatus
            word = word.replace('á.á', 'á').replace('á.a', 'á').replace('a.á', 'á').replace('a.a', 'á')
            word = word.replace('é.é', 'é').replace('é.e', 'é').replace('e.é', 'é').replace('e.e', 'é')
            word = word.replace('ó.ó', 'ó').replace('ó.o', 'ó').replace('o.ó', 'ó').replace('o.o', 'ó')
            word = word.replace('í.í', 'í').replace('i.í', 'ii').replace('í.i', 'ji')
            for i in range(1, len(word)-1):
                try:
                    if (word[i] == '.' and word[i-1] in pgV and word[i+1] in pgV):
                        if word[i-1] in 'ií':
                            word = word[:i-1] + 'j' + word[i+1:]
                        elif word[i+1] in 'ií':
                            word = word[:i] + 'i' + word[i+2:]
                        elif word[i-1] == 'u':
                            word = word[:i-1] + 'w' + word[i+1:]
                        elif word[i+1] == 'u':
                            word = word[:i] + word[i+1:]
                        else:
                            word = word[:i] + word[i:]
                except:
                    pass
            # Change notation
            word = word.replace('áu', 'au').replace('éu', 'eu').replace('óu', 'ou')
            word = word.replace('ái', 'ai').replace('éi', 'ei').replace('ói', 'oi')
            # 0.3 Voicing of initial /p/ before long vowels
            if (word[0] == 'p' and word[1] in pgL):
                word = 'b' + word[1:]
            # 0.4 Parasitic /j/
            for i in range(2, len(word)-2):
                if (word[i] == '.' and word[i+1] == 'j' and word[i-1] in pgC):
                    if word[i-2] == 'a':
                        word = word[:i-2] + 'á.' + word[i-1] + word[i+1:]
                    elif word[i-2] == 'e':
                        word = word[:i-2] + 'é.' + word[i-1] + word[i+1:]
                    elif word[i-2] == 'o':
                        word = word[:i-2] + 'ó.' + word[i-1] + word[i+1:]
                    elif word[i-2] == 'i':
                        word = word[:i-2] + 'í.' + word[i-1] + word[i+1:]
        # AGE 1
        if (age_i <= 1 and age_f >= 1):
            # 1.1 Intervocalic voicing of voiceless stops
            for i in range(1, len(word)-1):
                if word[i-1] == '.': # a.ka cases
                    if (word[i-2] in pgV and word[i+1] in pgV):
                        if word[i] == 'p':
                            word = word[:i] + 'b' + word[i+1:]
                        elif word[i] == 't':
                            word = word[:i] + 'd' + word[i+1:]
                        elif word[i] == 'k':
                            word = word[:i] + 'g' + word[i+1:]
                if word[i+1] == '.': # ak.a cases
                    if (word[i-1] in pgV and word[i+2] in pgV):
                        if word[i] == 'p':
                            word = word[:i] + 'b' + word[i+1:]
                        elif word[i] == 't':
                            word = word[:i] + 'd' + word[i+1:]
                        elif word[i] == 'k':
                            word = word[:i] + 'g' + word[i+1:]
            # 1.2 Voicing of stops in nasal cluster
            for i in range(1, len(word)-1):
                if (word[i] == '.' and word[i-1] in 'mn' and word[i+1] in 'ptk'): # m.k cases
                    if word[i+1] == 'p':
                        word = word[:i+1] + 'b' + word[i+2:]
                    if word[i+1] == 't':
                        word = word[:i+1] + 'd' + word[i+2:]
                    if word[i+1] == 'k':
                        word = word[:i+1] + 'g' + word[i+2:]
                if (word[i] == '.' and word[i+1] in 'mn' and word[i-1] in 'ptk'): # k.m cases
                    if word[i-1] == 'p':
                        word = word[:i-1] + 'b' + word[i:]
                    if word[i-1] == 't':
                        word = word[:i-1] + 'd' + word[i:]
                    if word[i-1] == 'k':
                        word = word[:i-1] + 'g' + word[i:]
            # 1.3 Further vowel hiatus
            for i in range(1, len(word)-1):
                if (word[i] == '.' and word[i-1] in pgV and word[i+1] in pgV):
                    if word[i-1] in 'eé':
                        word = word[:i+1] + 'k' + word[i+1:] # epenthetic /k/
        # AGE 2
        if (age_i <= 2 and age_f >= 2):
            # 2.1 Nasal assimilation
            for i in range(1, len(word)-1):
                if word[i] == '.':
                    if (word[i-1] == 'n' and word[i+1] in 'pb'):
                        word = word[:i-1] + 'm' + word[i:]
                    elif (word[i-1] in 'pb' and word[i+1] == 'n'):
                        word = word[:i+1] + 'm' + word[i+2:]
            # 2.2 Gemination of voiceless stop clusters
            for i in range(1, len(word)-1):
                if (word[i] == '.' and word[i-1] in 'ptk' and word[i+1] in 'ptk'):
                    word = word[:i-1] + word[i+1] + word[i:]
            # 2.3 Voicing of /s/ preceding long vowels
            word = word.replace('s.s', 'S.S')
            word = word.replace('sá', 'zá').replace('sé', 'zé').replace('só', 'zó')
            word = word.replace('S.S', 's.s')
            # 2.4 /ju/ -> /xu/
            for i in range(0, len(word)-1):
                if (word[i] == 'j' and word[i+1] in 'uíi'):
                    if i != 0:
                        if word[i-1] not in pgC:
                            word = word[:i] + 'x' + word[i+1:]
                    if i == 0:
                        word = 'x' + word[i+1:]
        # AGE 3
        if (age_i <= 3 and age_f >= 3):
            # 3.1 Palatalisation of tj, sj, tí, kí, sí
            word = word.replace('tj', 'ch').replace('tí', 'chí').replace('ti', 'chi')
            word = word.replace('sj', 'sh').replace('sí', 'shí').replace('si', 'shi')
            word = word.replace('k.k', 'K.K')
            word = word.replace('kjé', 'ché').replace('kje', 'che').replace('kjí', 'chí').replace('kji', 'chi')
            word = word.replace('kí', 'chí').replace('ki', 'chi').replace('ké', 'ché').replace('ke', 'che')
            word = word.replace('K.K', 'k.k')
            # 3.2 Intervocalic spirantisation of voiced stops
            for i in range(1, len(word)-1):
                if word[i-1] == '.': # a.ga cases
                    if (word[i-2] in pgV and word[i+1] in pgV):
                        if word[i] == 'b':
                            word = word[:i] + 'v' + word[i+1:]
                        elif word[i] == 'd':
                            word = word[:i] + 'dh' + word[i+1:]
                        elif word[i] == 'g':
                            word = word[:i] + 'q' + word[i+1:]
                if word[i+1] == '.': # ag.a cases
                    if (word[i-1] in pgV and word[i+2] in pgV):
                        if word[i] == 'b':
                            word = word[:i] + 'v' + word[i+1:]
                        elif word[i] == 'd':
                            word = word[:i] + 'dh' + word[i+1:]
                        elif word[i] == 'g':
                            word = word[:i] + 'q' + word[i+1:]
            # 3.3 Intervocalic voicing of voiceless stops
            for i in range(1, len(word)-1):
                if word[i-1] == '.': # a.ka cases
                    if (word[i-2] in pgV and word[i+1] in pgV):
                        if word[i] == 'p':
                            word = word[:i] + 'b' + word[i+1:]
                        elif word[i] == 't':
                            word = word[:i] + 'd' + word[i+1:]
                        elif word[i] == 'k':
                            word = word[:i] + 'g' + word[i+1:]
                if word[i+1] == '.': # ak.a cases
                    if (word[i-1] in pgV and word[i+2] in pgV):
                        if word[i] == 'p':
                            word = word[:i] + 'b' + word[i+1:]
                        elif word[i] == 't':
                            word = word[:i] + 'd' + word[i+1:]
                        elif word[i] == 'k':
                            word = word[:i] + 'g' + word[i+1:]
        # AGE 4
        if (age_i <= 4 and age_f >= 4):
            # 4.1 Spirantisation of word initial /p/ before short vowels
            if (word[0] == 'p' and word[1] in pgS+pgLiq):
                word = 'f' + word[1:]
            # 4.2 Loss of word-final short vowels
            if ('.' in word and word[-1] in pgS and word[-2] not in 'rw'): # add double consonant rule?
                if word[-4] not in pgC+'.':
                    word = word[:-1]
                    syll = word.split('.')
                    word = '.'.join(syll[:-1]) + syll[-1]
            # 4.3 Shortening of word-final long vowels
            if ('.' in word and word[-1] in pgL):
                if word[-1] == 'á':
                    word = word[:-1] + 'a'
                elif word[-1] == 'é':
                    word = word[:-1] + 'e'
                elif word[-1] == 'ó':
                    word = word[:-1] + 'o'
            # 4.4 Centralisation of word-final í /i/
            if ('.' in word and word[-1] == 'í'):
                word = word[:-1] + 'i'
            # 4.5 Devoicing of word-final stops
            if word[-1] in 'bdg':
                if word[-1] == 'b':
                    word = word[:-1] + 'p'
                elif word[-1] == 'd':
                    word = word[:-1] + 't'
                elif word[-1] == 'g':
                    word = word[:-1] + 'k'
    # Raise error if language code not recognised
    else:
        raise ValueError('Evolution path not recognised.')
    # Return evolved entry
    return word


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
    if path in [path_dic['IS'], path_dic['EVO']]:
        print(plex.sort_values('Orthography'))
    elif path == path_dic['FAU']:
        print(plex.sort_values('Name'))
    # Raise error if language code not recognised
    else:
        raise ValueError('Evolution path not recognised.')


def upd(path):
    # Get lexicon
    try:
        lex = pd.read_csv(path, sep=r'\t', engine='python')
    except:
        raise ValueError('Error loading CSV.')
    # Build new lexicon
    lex_new = pd.DataFrame(columns=list(lex.columns))

    #...

    # Export CSV lexicon
    lex_new.to_csv(lex_path, sep='\t', index=False)


def evo(path, entry, lang, age_i, age_f):
    # Take whole lexicon if entry == 'all'
    if entry == 'all':
        try:
            lex = pd.read_csv(path, sep=r'\t', engine='python')
        except:
            raise ValueError('Error loading CSV.')
    else:
        # Get IPA
        ipa = trans_ipa(entry, lang=lang, age=age_i)
        # Create entry and lexicon
        ne = {
            'Orthography' : entry,
            'IPA' : ipa,
            'Stress' : find_stress(ipa),
            'Hláhu' : '',
            'Age' : age_i,
            'Class' : '',
            'Description' : ''
        }
        lex = pd.DataFrame([pd.Series(ne)])
    # Create empty evolved lexicon
    evolex = pd.DataFrame(columns=list(lex.columns))
    # Iterate over all entries
    for index, series in lex.iterrows():
        # Get evolved word
        new = evolver(series['Orthography'], series['Age'], age_f, lang=lang)
        # Get IPA
        ipa_new = trans_ipa(new, lang)
        # Create entry
        ne = {
            'Orthography' : new,                                    # Evolved orthography
            'IPA' : ipa_new,                                        # Evolved IPA
            'Stress' : find_stress(ipa_new, lang),                  # Stress
            'Hláhu' : series['Hláhu'],                              # Hláhu (NG not included)
            'Age' : int(series['Age']),                                     # Final age
            'Class' : series['Class'],                              # Class
            'Description' : series['Description'],                  # Description
            'OG Ortho' : series['Orthography'],                     # Original orthography
            'OG IPA' : trans_ipa(series['Orthography'], lang),      # Original IPA
            'Changed' : str(new != series['Orthography'])           # Changed (boolean string)
        }
        # Append evolved entry to evolved lexicon
        evolex = evolex.append(ne, ignore_index=True)
    # Save evolved lexicon
    if entry == 'all':
        evolex.to_csv(path_dic['EVO'], sep=';', index=False)
    # Print result
    pd.set_option('display.max_rows', 999)
    print(evolex)

#-------------------------------------------------------------------------------
# MODE FUNCTION
#-------------------------------------------------------------------------------
# Select correct lexicon path
if lang.lower() in ['is', 'isk', 'iskélis', 'iskeelis']:
    path = path_dic['IS']
elif lang.lower() in ['hl', 'hlá', 'hla', 'hláhu', 'fau', 'fauja']:
    path = path_dic['FAU']
elif lang.lower() in ['evo', 'evolved', 'evolve']:
    path = path_dic['EVO']
# Raise error if language code not recognised
else:
    raise ValueError('Language code not recognised.')

# Run correct function according to mode
if mode in ['add', 'a']:
    add(path, entry)
elif mode in ['rem', 'remove', 'r']:
    rem(path, id)
elif mode in ['lst', 'list', 'l']:
    lst(path, axis, search, ran_num)
elif mode in ['upd', 'update', 'u']:
    upd(path)
elif mode in ['evo', 'evolve', 'e']:
    evo(path, entry, lang, age_i, age_f)
else:
    print('Action mode not recognised, please check your input')
    print('Avalable modes: add, rem, lst, upd, evo')
