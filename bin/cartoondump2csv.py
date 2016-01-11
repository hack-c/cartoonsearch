

"""
The data is in a tab delimited file with no newlines.

If you translate the tabs into newlines, you get this:

    100507
    100507 AFU Alfred Frueh Co-operation (Man cleaning windows of a subway car. Sign says: 'Please! Help Us Keep the 'L' and Subway Clean.")  car clean cleaning cleans community commute commuter commuters commuting cooperation dirty help keep man metro-north notice please public sanitation says service sign subway subways train trains transportation us window windows
    Co-operation
    100508925
    100508 AFU Alfred Frueh The Tower of Pisa in a Nervous Household (Man brings home picture of the Leaning Tower of Pisa, and everything in the room tilts the same way.)  af▒iction anxiety architecture art brings everything families family home homes household houses italian italians italy landmark leaning life man medieval monument nerves nervous picture pictures pisa print room same tilts tower towers way
    The Tower of Pisa in a Nervous Household
    100512925
    100512 WMO Wallace Morgan The Bread Line (Women waiting for entrance into a dining hall.) attraction attractive boyfriend bread charity chase couple couples cuisine date dates dating depression dining eating enteric ▒irt ▒irting food girlfriend girlfriends great hall hit hitting into line meal meals poverty relationship relationships restaurant restaurants sex sexual waiting women
    The Bread Line

Where the schema is:

- Cartoon ID
- Description / Keywords
- Caption

And these three-line (or four-line, sometimes there's a date) groups are repeated. 

There's also a heck of a lot of weird unicode stuff going on. Possibility to use unidecode, or perhaps python 3 will handle it automagically.

Game plan:
- Munge tsv into a clean csv form where characters have been corrected or at least stripped of mystery characters
- Create pipeline to documentize. Probably want word sets minus stop words
- Get LDA vectors
- Build Annoy index
- Query and tweak pipeline
- Get images
- Serve somehow
"""
import os
import re
import sys
import collections
import pandas as pd
from tqdm import tqdm
from joblib import delayed
from joblib import Parallel
from unidecode import unidecode

ROOT_DIR       = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
DATA_DIR       = os.path.join(ROOT_DIR, "data")
RAW_DIR        = os.path.join(DATA_DIR, "raw")
PROC_DIR       = os.path.join(DATA_DIR, "processed")


################[ peter norvig's spellchecker! ]################

def words(text): return re.findall('[a-z]+', text.lower()) 

def train(features):
    model = collections.defaultdict(lambda: 1)
    for f in features:
        model[f] += 1
    return model

NWORDS = train(words(open(os.path.join(RAW_DIR, 'big.txt'),'r').read()))

alphabet = 'abcdefghijklmnopqrstuvwxyz'

def edits1(word):
    splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes    = [a + b[1:] for a, b in splits if b]
    transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
    replaces   = [a + c + b[1:] for a, b in splits for c in alphabet if b]
    inserts    = [a + c + b     for a, b in splits for c in alphabet]
    return set(deletes + transposes + replaces + inserts)

def known_edits2(word):
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)

def known(words): return set(w for w in words if w in NWORDS)

def correct(word):
    candidates = known([word]) or known(edits1(word)) or known_edits2(word) or [word]
    return max(candidates, key=NWORDS.get)

def correct_line(t):
    return ' '.join(map(correct, words(t))) if pd.notnull(t) else t


################[ asciidammit is a straight rip from the fuzzywuzzy source ]################

bad_chars = str("").join([chr(i) for i in range(128, 256)])  # ascii!!
PY3 = sys.version_info[0] == 3
if PY3:
    translation_table = dict((ord(c), None) for c in bad_chars)


def asciionly(s):
    if PY3:
        return s.translate(translation_table)
    else:
        return s.translate(None, bad_chars)


def asciidammit(s):
    if type(s) is str:
        return unicode(asciionly(s))
    elif type(s) is unicode:
        return asciionly(s.encode('ascii', 'ignore'))
    else:
        return asciidammit(unicode(s))



if __name__ == '__main__':

    print("munging file to csv", end='\n')

    datepattern = re.compile(r"^(19|20)\d\d[- /.](0[1-9]|1[012])[- /.](0[1-9]|[12][0-9]|3[01])$")

    with open(os.path.join(PROC_DIR, 'cartoondump_newlines.txt'),'r', encoding="ISO-8859-2") as dumpfile:
        with open(os.path.join(PROC_DIR, 'cartoondump_clean.csv'),'w') as outfile:
            l=0
            for line in tqdm(dumpfile):
                try:
                    line = unidecode(line)
                except UnicodeDecodeError:
                    line = asciidammit(line)
                line = line.lower().strip()

                if not re.match(r'^[0-9]{4,}$', line):
                    outfile.write(' ' + line)
                else:
                    outfile.write('\n' + line + '|')
                    l+=1

    print("complete.", end='\n')
    print("got {} lines.".format(l))

    print("reading cleaned csv...")
    df = pd.read_csv(os.path.join(PROC_DIR, 'cartoondump_clean.csv'), sep='|', names=['id','text'])

    print("lowercasing...")
    docs = df.text.str.lower().str.strip()

    print("correcting...")

    corrected = []
    for d in tqdm(docs):
        corrected.append(correct_line(d))

    df['document'] = pd.Series(corrected)

    df.to_csv('documents.csv', index=False)

    print("done.")



