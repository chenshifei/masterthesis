import argparse
from spacy.lang.xx import MultiLanguage

parser = argparse.ArgumentParser(description='Tokenize the corpus and build its vocabulary.')
parser.add_argument('corpus', help='Path to the corpus file.')
parser.add_argument('--out', help='Path to the output vocabulary file. Default is out.vocab', default='out.vocab')
args = parser.parse_args()

nlp = MultiLanguage()
vocab = set()
with open(args.corpus, 'r') as fin:
    doc = nlp(fin.read())
    vocab = set([tok.text for tok in doc])
vocab = sorted(vocab)
with open(args.out, 'w') as fout:
    fout.write('\n'.join(vocab))
