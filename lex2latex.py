"""
LINUX:
Use in shell as: 'python3 Python/lex2latex.py | xclip'
It copies the output to your MIDDLE-MOUSE clipboard.
"""

# Imports
import numpy as np
import pandas as pd

# Import lexicon.csv using Pandas
lex = pd.read_csv('./data/lexicon.tsv',delimiter='\t')

# Sort on Orthography
lexsrt = lex.sort_values('Orthography')

# Get unique first characters
uni, cnt = np.unique([i[0] for i in list(lexsrt['Orthography'])], return_counts=True)

# Print LaTeX code
for u in uni:
    # Print \section
    print(r'\section*{{{}}}'.format(u))
    # Open \multicols
    print(r'\begin{multicols}{3}')
    # Cut lexicon
    lexcut = lexsrt[np.array([i[0] for i in list(lexsrt['Orthography'])]) == u]
    for index, row in lexcut.iterrows():
        # Print dictionary entry
        print(r'\entry {{{}}}{{[{}]}}{{\pos {}. \definition {}}}'.format( \
              row['Orthography'], row['IPA'], row['Class'], row['Description']))
    # Close \multicols
    print(r'\end{multicols}')
    # Spacing
    print(r'\needspace{15\baselineskip}')
