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

def prune_embedding(emb, vocab_paths):
    new_emb = {}
    for path in vocab_paths:
        vocab = load_vocab(path)
        for word in vocab:
            if emb.get(word):
                new_emb = emb[word]
    return new_emb

def write_embedding(emb, path):
    with open(path, 'w') as f:
        f.write(f'{len(emb)} 300\n')
        for word, vectors in emb.items():
            f.write(f"{word} {' '.join(vectors)}\n")

def load_vocab(vocab_path):
    result = []
    with open(vocab_path) as f:
        result = [line for line in f.readlines()]
    return result

parser = argparse.ArgumentParser(
    description='Prune the word embedding files by entries from the vocab files')
parser.add_argument('emb', help='Path to the embedding file')
parser.add_argument('vocabs', nargs='+', help='Paths to the vocab files')
parser.add_argument('--output',
                    help='Path to the output file, default = merged_emb.vec',
                    default='merged_emb.vec')
args = parser.parse_args()

original_emb = load_embedding(args.emb)
final_emb = prune_embedding(original_emb, args.vocabs)
write_embedding(final_emb, args.output)
