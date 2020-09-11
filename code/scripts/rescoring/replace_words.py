import argparse
import string
import re
import numpy as np
from itertools import islice
from scipy import spatial

def load_embedding(emb_path, insert_lang_id=False):
    result = dict()
    with open(emb_path, encoding='utf8') as emb_file:
        for line in islice(emb_file, 1, None):
            record = line.split(' ', 1)
            word = record[0]
            result[word] = np.fromstring(record[1], sep=' ')
    return result

def replace_words(hyp_path, output_path, src_emb_path, tgt_emb_path):
    src_emb = load_embedding(src_emb_path)
    tgt_emb = load_embedding(tgt_emb_path)
    tgt_vecs = np.array(list(tgt_emb.values()))
    tree = spatial.KDTree(tgt_vecs)

    with open(output_path, 'w') as output_file:
        with open(hyp_path, encoding='utf8') as hyp_file:
            for line in hyp_file:
                result = ''
                if ARGS.langid and line.startswith(ARGS.langid):
                    result = line
                else:
                    result = _replace_words_in_line(line, src_emb, tgt_emb, tree)
                    result += '\n'
                output_file.write(result)

def _replace_words_in_line(line, src_emb, tgt_emb, tree):
    result = []
    tgt_emb_words = list(tgt_emb.keys())
    for word in line.split():
        if _should_skip_replacement(word, src_emb):
            result.append(word)
        elif DIST_CACHE.get(word) is not None:
            result.append(DIST_CACHE[word])
        else:
            src_vec = src_emb[word]
            distance, index = tree.query(src_vec)
            target_word = word
            if ARGS.threshold == 0 or distance < ARGS.threshold:
                target_word = tgt_emb_words[index] # From Python 3.7 dict is ordered.
            result.append(target_word)
            DIST_CACHE[word] = target_word
    return ' '.join(result)

def _should_skip_replacement(word, src_emb):
    if len(word) <= 1 and word in string.punctuation:
        return True
    elif re.match(r'__[a-zA-Z]{2}__', word):
        return True
    elif word == '<unk>':
        return True
    elif src_emb.get(word) is None:
        return True
    else:
        return False

parser = argparse.ArgumentParser(
    description='Search the translation output word and replace it to the closest word in the target embedding file.')
parser.add_argument('hyp', help='Path to the hypothesis translation output')
parser.add_argument('src_emb', help='Path to the embedding file where the translation hypothesis was inferred')
parser.add_argument('tgt_emb', help='Path to the embedding file whose word vectors the inferred translation word should be compared with')
parser.add_argument('--threshold', help='Minimum distance threshold between two word embddings so that they are considered to be equivalent. Set it to 0 to disable threshold. Default = 2.', default=2, type=float)
parser.add_argument('--langid', help='Specify the language to be replaced. Useful for process translation input source.')
parser.add_argument('--output',
                    help='Path to the output file, default = filtered.test_hyp',
                    default='filtered.test_hyp')
ARGS = parser.parse_args()
DIST_CACHE = dict()
replace_words(ARGS.hyp, ARGS.output, ARGS.src_emb, ARGS.tgt_emb)
