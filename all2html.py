# Imports
import numpy as np
import pandas as pd

# ------------------------------------------------------------------------------
# LEXICON PRINTER
# ------------------------------------------------------------------------------
# Lex modes
lex_modes = ['lex', 'evo']

# Defined order of the alphabet
alphabet = ['a', 'á', 'b', 'c', 'd', 'e', 'é', 'f', 'g', 'h', 'i', 'í', 'j', 'k', 'l', 'hl',
            'm', 'n', 'o', 'ó', 'p', 'q', 'r', 's', 'sh', 't', 'tl', 'ch', 'u', 'v',
            'w', 'x', 'y', 'z']

for mode in lex_modes:
    # Import the correct lexicon.csv using Pandas
    if mode == 'lex':
        lex = pd.read_csv('./data/iskeelis.tsv', delimiter='\t')
        f = open('../../Webpage/public_html/tables/ISKlist.html', 'wb')
    elif mode == 'evo':
        lex = pd.read_csv('./data/evolved.tsv', delimiter='\t')
        f = open('../../Webpage/public_html/tables/EVOlist.html', 'wb')
    else:
        raise ValueError('Type not recognised, please use lex or evo.')
    lex = lex.replace(np.nan, ' ', regex=True)

    # Print table
    f.write(b'<table class="tg" style="undefined;table-layout: fixed; width: 903px">')
    f.write(b'<colgroup>')
    f.write(b'<col style="width: 301px">')
    f.write(b'<col style="width: 301px">')
    f.write(b'<col style="width: 301px">')
    f.write(b'</colgroup>')
    f.write(b'<tbody>')
    # For each letter in the alphabet
    for i in range(len(alphabet)):
        if alphabet[i] == 'c':
            sublex = lex[(lex['Orthography'].astype(str).str[0] == 'c') &
                         (lex['Orthography'].astype(str).str[1] != 'h')]
        elif alphabet[i] == 'h':
            sublex = lex[(lex['Orthography'].astype(str).str[0] == 'h') &
                         (lex['Orthography'].astype(str).str[1] != 'l')]
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
            sublex = lex[(lex['Orthography'].astype(str).str[0] == 'c') &
                         (lex['Orthography'].astype(str).str[1] == 'h')]
        else:
            sublex = lex[lex['Orthography'].astype(str).str[0] == alphabet[i]]

        # Print section
        if len(sublex.index) != 0:
            f.write(b'<tr>')
            f.write('<td class="tg-wp8o" colspan="3">{0}</td>'.format(alphabet[i]).encode('ascii', 'xmlcharrefreplace'))
            f.write(b'</tr>')

            j = 0
            # Print according entries
            for index, entry in sublex.iterrows():
                if j % 3 == 0:
                    f.write(b'<tr>')
                f.write('<td class="tg-73oq"><span style="font-weight:bold;color:#1d77a8">{0}</span> [{1}]<br>    <span style="font-style:italic">{2}.</span> {3}</td>'
                        .format(entry['Orthography'].replace('.', ''), entry['IPA'], entry['Class'], entry['Description'].lower()).encode('ascii', 'xmlcharrefreplace'))
                if j % 3 == 2:
                    f.write(b'</tr>')
                j += 1

    f.write(b'</tbody>')
    f.write(b'</table>')
    # Close file
    f.close()

# ------------------------------------------------------------------------------
# HLAAHU PRINTER
# ------------------------------------------------------------------------------
# Import lexicon.csv using Pandas
lex = pd.read_csv('./data/hlaahu.tsv',delimiter='\t')
lex = lex.replace(np.nan, ' ', regex=True)

evo_modes = ['OG', 'NG']

for mode in evo_modes:
    if mode == 'OG':
        cut_lex = lex[lex['NG'] == ' ']
        f = open('../../Webpage/public_html/tables/OGlist.html', 'wb')
    elif mode == 'NG':
        cut_lex = lex[lex['NG'] != ' ']
        f = open('../../Webpage/public_html/tables/NGlist.html', 'wb')
    else:
        raise ValueError('Type not recognised, please use OG or NG.')

    # Sort on Orthography
    lexsrt = cut_lex.sort_values('Name')

    # Print HTML table for list view
    # Print header
    f.write(b'<table id="tg-peUr8" class="tg">')
    f.write(b'<thead>')
    f.write(b'  <tr>')
    f.write('    <th class="tg-6t95">Hláhu</th>'.encode('ascii', 'xmlcharrefreplace'))
    if type == 'NG':
        f.write(b'    <th class="tg-6t95">Origin</th>')
    f.write(b'    <th class="tg-6t95">Name</th>')
    f.write('    <th class="tg-6t95">Nerlé</th>'.encode('ascii', 'xmlcharrefreplace'))
    f.write('    <th class="tg-6t95">Óle</th>'.encode('ascii', 'xmlcharrefreplace'))
    f.write(b'    <th class="tg-ru17">Description</th>')
    f.write(b'    <th class="tg-6t95">Evo. Name</th>')
    f.write(b'    <th class="tg-6t95">Evo. Nerle</th>')
    f.write('    <th class="tg-6t95">Evo. Ól</th>'.encode('ascii', 'xmlcharrefreplace'))
    f.write(b'  </tr>')
    f.write(b'</thead>')
    # Print body
    f.write(b'<tbody>')
    for index, entry in lexsrt.iterrows():
        # f.write(bindex)
        f.write(b'  <tr>')
        f.write('    <td class="tg-baqh"><img src="../img/hlaahu/{0:03}.png" alt="Image" width="100" height="100"></td>'.format(int(entry['NO.'])).encode('ascii', 'xmlcharrefreplace'))
        if type == 'NG':
            e1, e2 = entry['NG'].split(', ')
            f.write('    <td class="tg-baqh"><img src="../img/hlaahu/{0:03}.png" alt="Image" width="60" height="60"><img src="../img/hlaahu/{1:03}.png" alt="Image" width="60" height="60"></td>'
                    .format(int(lex[lex['Name'] == e1].iloc[0]['NO.']), int(lex[lex['Name'] == e2].iloc[0]['NO.'])).encode('ascii', 'xmlcharrefreplace'))
        f.write('    <td class="tg-baqh">{}</td>'.format(entry['Name']).encode('ascii', 'xmlcharrefreplace'))
        f.write('    <td class="tg-5frq">{}</td>'.format(entry['Nerlé']).encode('ascii', 'xmlcharrefreplace'))
        f.write('    <td class="tg-5frq">{}</td>'.format(entry['Óle']).encode('ascii', 'xmlcharrefreplace'))
        f.write('    <td class="tg-0lax">{}</td>'.format(entry['Description']).encode('ascii', 'xmlcharrefreplace'))
        f.write('    <td class="tg-baqh">{}</td>'.format(entry['Evo. Name']).encode('ascii', 'xmlcharrefreplace'))
        f.write('    <td class="tg-5frq">{}</td>'.format(entry['Evo. Nerle']).encode('ascii', 'xmlcharrefreplace'))
        f.write('    <td class="tg-5frq">{}</td>'.format(entry['Evo. Ól']).encode('ascii', 'xmlcharrefreplace'))
        f.write(b'  </tr>')
    f.write(b'</tbody>')
    f.write(b'</table>')
    # Close file
    f.close()

# ------------------------------------------------------------------------------
# BLOCK PRINTER
# ------------------------------------------------------------------------------
    if mode == 'OG':
        f = open('../../Webpage/public_html/tables/FAUblock.html', 'wb')
        f.write(b'<h2>List of Hl&#225;hu of Isk&#233;lis</h2>')
    elif mode == 'NG':
        f = open('../../Webpage/public_html/tables/FAUblock.html', 'ab')
        f.write(b'<h2>List of New Generation combinations</h2>')
    # Print all images for block view
    for index, entry in lexsrt.iterrows():
        f.write('  <img src="../img/hlaahu/{0:03}.png" width="100" height="100">'.format(int(entry['NO.'])).encode('ascii', 'xmlcharrefreplace'))
    # Close file
    f.close()
