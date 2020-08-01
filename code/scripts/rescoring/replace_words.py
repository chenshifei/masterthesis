import argparse
import string
import numpy as np
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

    with open(output_path) as output_file:
        with open(hyp_path, encoding='utf8') as hyp_file:
            for line in hyp_file:
                result = _replace_words_in_line(line, src_emb, tgt_emb)
                output_file.write(result)

def _replace_words_in_line(line, src_emb, tgt_emb):
    result = ''
    for word in line.split():
        if len(word) <= 1 and word in string.punctuation:
            result += word
        else if DIST_CACHE[word]:
            result += DIST_CACHE[word]
        else:
            src_vec = src_emb[word]
            tgt_vecs = np.array(list(tgt_emb.values()))
            tree = spatial.KDTree(tgt_vecs)
            distance, index = tree.query(src_vec)
            target_word = word
            if distance < ARGS.dist_threshold:
                target_word = tgt_emb.keys()[index] # From Python 3.7 dict is ordered.
            result += target_word
            DIST_CACHE[word] = target_word
    return result

parser = argparse.ArgumentParser(
    description='Search the translation output word and replace it to the closest word in the target embedding file.')
parser.add_argument('hyp', help='Path to the hypothesis translation output')
parser.add_argument('src_emb', help='Path to the embedding file where the translation hypothesis was inferred')
parser.add_argument('tgt_emb', help='Path to the embedding file whose word vectors the inferred translation word should be compared with')
parser.add_argument('--dist_threshold', help=='minimum distance threshold between two word embddings to be replaced.', default=5, type=int)
parser.add_argument('--output',
                    help='Path to the output file, default = test_filtered.hyp',
                    default='test_filtered.hyp')
ARGS = parser.parse_args()
DIST_CACHE = dict()
