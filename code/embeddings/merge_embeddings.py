import argparse
from itertools import islice

def load_embedding(emb_path):
    result = dict()
    with open(emb_path, encoding="utf8") as emb_file:
        for line in islice(emb_file, 1, None):
            records = line.split(' ')
            word = records[0]
            result[word] = map(float, records[1:])
    return result

def merge_embedding(emb_paths):
    first_emb = load_embedding(emb_paths[0])
    for emb_path in emb_paths[1:]:
        emb = load_embedding(emb_path)
        for w in emb.keys():
            if first_emb.get(w):
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
    result = []
    for da, db in zip(a, b):
        d = (da + db) / 2
        result.append(d)
    return result

parser = argparse.ArgumentParser(
    description='Merge the word embedding files')
parser.add_argument('emb', help='Path to the embedding file', nargs='+')
parser.add_argument('--output',
                    help='Path to the output file, default = merged_emb.vec',
                    default='merged_emb.vec')
args = parser.parse_args()

emb = merge_embedding(args.emb)
write_embedding(emb, args.output)
