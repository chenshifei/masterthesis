import argparse
from itertools import islice
import string
import numpy as np

def load_embedding(emb_path, insert_lang_id=False):
    result = dict()
    with open(emb_path, encoding="utf8") as emb_file:
        lang_id = extract_lang_id(emb_path)
        for line in islice(emb_file, 1, None):
            record = line.split(' ', 1)
            word = record[0]
            if insert_lang_id:
                word = prefix_word_with_lang_id(word, lang_id)
            result[word] = np.fromstring(record[1], sep=' ')
    return result

def extract_lang_id(emb_path):
    components = emb_path.split('.')
    if len(components) < 3:
        return ""
    result = components[1]
    if len(result) > 3 or '+' in result:
        return ""
    return result

def prefix_word_with_lang_id(word, lang_id):
    if len(word) == 1 or not lang_id or word.startswith('<<'):
        return word
    return f'<<{lang_id}>>{word}'

def merge_embedding(emb_paths, insert_lang_id=False):
    first_emb = load_embedding(emb_paths[0])
    for emb_path in emb_paths[1:]:
        emb = load_embedding(emb_path, insert_lang_id)
        for w in emb.keys():
            if first_emb.get(w) is not None:
                first_emb[w] = _average_vectors(first_emb[w], emb[w])
            else:
                first_emb[w] = emb[w]
    return first_emb

def write_embedding(emb, path):
    with open(path, 'w') as f:
        f.write(f'{len(emb)} 300\n')
        for word, vectors in emb.items():
            f.write(word)
            for d in vectors:
                f.write(f' {d:.4f}')
            f.write('\n')

def _average_vectors(a, b):
    return np.average(np.array([a, b]), axis=0)

parser = argparse.ArgumentParser(
    description='Merge the word embedding files')
parser.add_argument('emb', help='Path to the embedding file', nargs='+')
parser.add_argument('--langid', 
                    help='Insert lang id from each of the embedding file to the every word in the final merged embeddings, default = False',action='store_true')
parser.add_argument('--output',
                    help='Path to the output file, default = merged_emb.vec',
                    default='merged_emb.vec')
args = parser.parse_args()

emb = merge_embedding(args.emb, args.langid)
write_embedding(emb, args.output)
